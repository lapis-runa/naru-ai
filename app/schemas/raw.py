from pydantic import BaseModel
from datetime import date as date_type
from typing import Optional


# 保存リクエストで受け取る形。
# id / hash / date は任意(無ければサーバーが補完する)。content は必須。
class RawEntryCreate(BaseModel):
    content: str                          # 本文(必須)
    source: str = "diary"                 # 種別。省略時は diary
    id: Optional[str] = None              # 送られたら使う、無ければ生成
    hash: Optional[str] = None            # 送られたら使う、無ければ生成
    date: Optional[date_type] = None      # 送られたら使う、無ければ今日
    title: Optional[str] = None           # 任意


# APIから返す形。
class RawEntryResponse(BaseModel):
    id: str
    date: date_type
    source: str
    content: str
    hash: str
    title: Optional[str] = None

    class Config:
        from_attributes = True