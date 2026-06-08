# なる専用思考AI（naru-ai）

> 自分の思考を保存・整理・拡張するための、ローカル AI 基盤。
> AI は補助者であり主体ではない。最終判断は必ず自分が下す。

個人の日記・メモ・対話ログを一次資料（Raw）として完全保存し、AI で構造化（Processed）、
さらに「感情の動きのかたまり」（Episode）として束ねていく三層アーキテクチャの思考支援システムです。
個人データはローカルに閉じ、外部 LLM には送らない設計を中核に置いています。

設計の詳細は `docs/` の設計仕様書・議事録を参照してください。

---

## 設計思想

- **思考を支配しない AI** — AI の出力は仮説でしかない。むしろ「ズレ」が価値になる。
- **生データを持っておけば、アルゴリズムは後から変えられる** — Raw 層は不変。加工層は何度でも作り直せる。
- **プライバシーは設計で守る** — 日記の本文はローカルの SQLite / ChromaDB にのみ存在。外部 API には個人データを渡さない。

---

## アーキテクチャ：三層分離構造

```
Raw  →  Processed  →  Episode
原本     AI 加工       遷移記録
```

| 層 | 役割 | 状態 |
| --- | --- | --- |
| **Raw** | 思考の一次資料。改変しない・完全保存。SHA-256 で改ざん検知 | 実装済み |
| **Processed** | Raw を元に AI が感情座標（valence / arousal）や類型を自動生成 | スキーマのみ（カラムは確保済み・推定処理は未実装） |
| **Episode** | 複数エントリにまたがる感情の軌跡を一単位として保存 | 設計のみ |

上位層は下位層を書き換えません。Processed を丸ごと削除して再生成する「リプロセス運用」を前提にしています。

---

## 技術スタック

| 役割 | 採用技術 |
| --- | --- |
| バックエンド | Python 3.12 + FastAPI + SQLAlchemy |
| メタデータ DB | SQLite |
| ベクトル DB | ChromaDB |
| 埋め込みモデル | bge-m3（`sentence-transformers`） |
| ローカル LLM 実行 | Ollama |
| フロントエンド | Next.js 16 + React 19 + TypeScript |
| 依存管理 | uv（Python） / npm（Node） |

「8GB VRAM（RTX 4060 Ti）」という制約下で動かすため、モデルは同時ロードせずタスクごとにスワップする運用を想定しています。

---

## 現在できること

- 日記の保存（`POST /entries/`）— id・hash・date を省略するとサーバー側で補完
- キーワード検索（`GET /entries/search`）
- 期間検索（`GET /entries/range`）— 「時間軸対話モード」の SQL 版
- 意味検索（`GET /entries/semantic`）— bge-m3 + ChromaDB。言葉が違っても意味が近い日記を引く
- 一覧・1件取得（`GET /entries/recent` / `GET /entries/{id}`）
- 既存日記（約 424 件）の一括ベクトル化（`scripts/build_vectors.py`）
- フロント：投稿・検索・記事閲覧の各画面

---

## ディレクトリ構成

```
naru-ai/
├── app/                  # バックエンド（FastAPI）
│   ├── main.py           # エントリポイント・CORS・ルーター登録
│   ├── api/raw.py        # /entries エンドポイント群
│   ├── crud/raw.py       # DB 操作（保存・検索・取得）
│   ├── db/
│   │   ├── database.py   # エンジン・セッション
│   │   └── models.py     # raw_entries テーブル定義
│   ├── schemas/raw.py    # Pydantic スキーマ（入出力の形）
│   ├── services/
│   │   ├── vector.py     # bge-m3 + ChromaDB（意味検索の中核）
│   │   └── processing.py # 感情推定など（未実装）
│   ├── core/config.py    # 設定（DATABASE_URL 等）
│   └── utils/hash.py     # SHA-256 ハッシュ生成・検証
├── frontend/             # Next.js（TypeScript）
│   └── app/              # write / search / entry 画面
├── scripts/
│   └── build_vectors.py  # 既存 SQLite → ChromaDB 流し込み
└── docs/                 # 設計仕様書・議事録・作業ログ
```

---

## セットアップ

### バックエンド

```bash
# 依存をインストール（uv を使用）
uv sync

# 開発サーバー起動
uv run uvicorn app.main:app --reload
# → http://localhost:8000  （API ドキュメント: /docs）
```

`.env`（任意。なければ既定値を使用）:

```
DATABASE_URL=sqlite:///./app/db/raw.sqlite
```

### 意味検索を有効にする

既存の日記をベクトル化して ChromaDB に登録します。初回は bge-m3（約 2GB）が自動ダウンロードされます。

```bash
uv run python scripts/build_vectors.py
```

### フロントエンド

```bash
cd frontend
npm install
npm run dev
# → http://localhost:3000
```

バックエンドの URL を変える場合は `frontend/.env.local` に `NEXT_PUBLIC_API_URL` を設定します。

---

## ロードマップ

設計（仕様書 v1.2 / 議事録 vol.1〜3）に対する実装の進捗です。

- [x] Raw 層：テーブル定義・保存・SHA-256 ハッシュ
- [x] キーワード／期間／意味検索
- [x] フロント：投稿・検索・閲覧
- [ ] Processed 層：Ollama で valence / arousal・entry_type を自動推定
- [ ] Episode 層：感情座標の軌跡（waypoints）の構築
- [ ] 軌跡検索（DTW）：心の動きの「形」が似た過去エピソードを引く
- [ ] ハイブリッド RAG：意味 × 属性 × 軌跡を組み合わせた壁打ち
- [ ] 思考モード切り替え（整理／掘り下げ／比較／逆張り／時間軸対話 等）
- [ ] SQLite → PostgreSQL 移行

---

## データの扱いについて

生の日記データ（`app/db/raw.sqlite`・`app/db/chroma_db/`）と `.env` は `.gitignore` で
リポジトリから除外しています。コードとプライベートデータは厳格に分離する方針です。
クラウドへ退避する場合は、暗号化したうえでアップロードしてください。
