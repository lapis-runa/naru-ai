"""
意味検索の中核: bge-m3(埋め込み) + ChromaDB(ベクトル保管・検索)。

文章を bge-m3 でベクトル化し、ChromaDB に貯め、意味が近いものを引く。
bge-m3 は初回呼び出し時にモデル(約2GB)を自動DL。RTX 4060 Ti なら GPU で高速。

遅延ロード: import しただけではモデルを読まない。最初に必要になった時だけ読む。
→ サーバー起動を速くし、保存だけの操作ではモデルを読み込まない。
"""

import chromadb
from pathlib import Path
from typing import Optional

# ChromaDBの保存先(SQLiteと同じ app/db/ 配下に置く)
CHROMA_PATH = Path(__file__).resolve().parents[1] / "db" / "chroma_db"

# モデル・クライアントは一度だけ読み込んで使い回す(グローバルにキャッシュ)
_model = None
_client = None
_collection = None


def _get_model():
    """bge-m3 を遅延ロード。最初の1回だけ実際に読み込む。"""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        print("[vector] bge-m3 をロード中...(初回はDLが走る)")
        _model = SentenceTransformer("BAAI/bge-m3")
        print("[vector] ロード完了")
    return _model


def _get_collection():
    """ChromaDBのコレクション(棚)を取得。無ければ作る。"""
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path=str(CHROMA_PATH))
        _collection = _client.get_or_create_collection(
            name="diaries",
            metadata={"hnsw:space": "cosine"},  # 近さの測り方=コサイン類似度
        )
    return _collection


def embed(text: str) -> list:
    """文章を1024次元ベクトルにする。返り値は普通のlist。"""
    vec = _get_model().encode(text, normalize_embeddings=True)
    return vec.tolist()


def add_entry(id_: str, content: str, metadata: dict) -> None:
    """1件をChromaDBに登録。id_ は SQLite の id と同じにする(連携の鍵)。"""
    col = _get_collection()
    col.add(
        ids=[id_],
        embeddings=[embed(content)],
        documents=[content],
        metadatas=[metadata],
    )


def search(query: str, n_results: int = 5, source: Optional[str] = None) -> list:
    """意味検索。query に近い意味の日記を n_results 件返す。"""
    col = _get_collection()
    where = {"source": source} if source else None
    res = col.query(
        query_embeddings=[embed(query)],
        n_results=n_results,
        where=where,
    )
    out = []
    if res["ids"] and res["ids"][0]:
        for i, _id in enumerate(res["ids"][0]):
            md = res["metadatas"][0][i] or {}
            doc = res["documents"][0][i] or ""
            dist = res["distances"][0][i]
            out.append({
                "id": _id,
                "date": md.get("date", ""),
                "source": md.get("source", ""),
                "title": md.get("title"),
                "snippet": doc[:80],
                "score": round(1 - dist, 4),
            })
    return out