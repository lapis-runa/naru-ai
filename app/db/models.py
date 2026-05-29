from sqlalchemy import Column, String, Date, Text, Integer, Float, DateTime, func
from app.db.database import Base


class RawEntry(Base):
    __tablename__ = "raw_entries"

    # 人間が読めるID: YYYYMMDD-HHMMSS-SOURCE
    id = Column(String, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    source = Column(String, nullable=False)   # diary / creative / memo / idea
    content = Column(Text, nullable=False)
    # フロントエンドで生成されたSHA-256ハッシュ
    hash = Column(String, nullable=False)

    # --- ここから下が今日の追記 ---

    # 任意のメタ情報。reaction系はchat_reaction用(仕様書2-1)
    reaction_context = Column(Text, nullable=True)
    reaction_type = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # pencakeインポート時の追跡用(原本には影響しない補助情報)
    chapter = Column(String, nullable=True)
    chapter_title = Column(String, nullable=True)
    article_no = Column(Integer, nullable=True)
    title = Column(String, nullable=True)

    # 層2(Processed)用。今はNULL。Ollamaで感情推定したら埋める。
    valence = Column(Float, nullable=True)      # 快/不快 -1.0〜1.0
    arousal = Column(Float, nullable=True)      # 覚醒度 0.0〜1.0
    entry_type = Column(String, nullable=True)  # resolved/continuing/pivoting/log