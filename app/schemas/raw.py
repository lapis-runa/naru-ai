from pydantic import BaseModel
from datetime import date

# 共通のフィールド
class RawEntryBase(BaseModel):
    id: str
    date: date
    source: str
    content: str
    hash: str

# データ作成時の型
class RawEntryCreate(RawEntryBase):
    pass

# APIから返却する時の型
class RawEntryResponse(RawEntryBase):
    class Config:
        from_attributes = True