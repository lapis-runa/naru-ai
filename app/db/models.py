from sqlalchemy import Column, String, Date, Text
from app.db.database import Base

class RawEntry(Base):
    __tablename__ = "raw_entries"

    # 人間が読めるID: YYYYMMDD-HHMMSS-SOURCE
    id = Column(String, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    source = Column(String, nullable=False)  # 例: diary, memo, pencake
    content = Column(Text, nullable=False)
    # フロントエンドで生成されたSHA-256ハッシュ
    hash = Column(String, nullable=False)