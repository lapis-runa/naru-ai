"""
既存の raw.sqlite(424件) を ChromaDB に流し込む。
これを実行すると、過去の全日記が意味検索の対象になる。

実行: cd ~/projects/naru-ai && uv run python scripts/build_vectors.py

注意:
  - bge-m3(約2GB)が初回DLされる。GPUがあれば数分、CPUのみだと数十分。
  - 本文が空の7件はスキップ(意味検索の対象外)。
  - 何度実行しても同じidは上書き(冪等)。失敗しても再実行できる。
"""

import sys
from pathlib import Path

# プロジェクトルートを import パスに追加(scripts/ から app/ を読むため)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db.database import SessionLocal
from app.db import models
from app.services import vector


def main():
    db = SessionLocal()
    rows = db.query(models.RawEntry).order_by(models.RawEntry.date).all()
    db.close()

    total = len(rows)
    print(f"対象: {total} 件をベクトル化します")

    col = vector._get_collection()
    BATCH = 32
    buf_ids, buf_emb, buf_doc, buf_md = [], [], [], []
    done = 0

    for r in rows:
        content = r.content or ""
        if content.strip() == "":
            done += 1
            continue
        buf_ids.append(r.id)
        buf_emb.append(vector.embed(content))
        buf_doc.append(content)
        buf_md.append({
            "date": r.date.isoformat() if r.date else "",
            "source": r.source or "",
            "title": r.title or "",
        })
        if len(buf_ids) >= BATCH:
            col.add(ids=buf_ids, embeddings=buf_emb,
                    documents=buf_doc, metadatas=buf_md)
            done += len(buf_ids)
            print(f"  {done}/{total} 完了")
            buf_ids, buf_emb, buf_doc, buf_md = [], [], [], []

    if buf_ids:
        col.add(ids=buf_ids, embeddings=buf_emb,
                documents=buf_doc, metadatas=buf_md)
        done += len(buf_ids)

    print(f"完了: ChromaDB に登録しました(本文空はスキップ)")


if __name__ == "__main__":
    main()