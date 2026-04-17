import os
from dotenv import load_dotenv

# .env ファイルを読み込む
load_dotenv()

class Settings:
    # データベースの接続先。環境変数になければデフォルト値を使う
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app/db/raw.sqlite")

# ここでインスタンス化（実体化）して、外部から import settings できるようにする
settings = Settings()