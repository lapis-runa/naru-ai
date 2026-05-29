from sqlalchemy.orm import Session
from datetime import datetime
from app.db import models
from app.schemas import raw as schemas
from app.utils.hash import make_hash


def _make_unique_id(db: Session, base: str) -> str:
    """
    base(例 20260529-153000-diary) が既にDBにあれば -2,-3... を付けて一意化。
    今日のpencake投入スクリプトと同じ衝突回避の考え方。
    """
    candidate = base
    n = 1
    while db.query(models.RawEntry).filter(models.RawEntry.id == candidate).first() is not None:
        n += 1
        candidate = f"{base}-{n}"
    return candidate


def create_raw_entry(db: Session, entry: schemas.RawEntryCreate):
    now = datetime.now()

    # --- date: 送られなければ今日 ---
    entry_date = entry.date if entry.date is not None else now.date()
    date_str = entry_date.isoformat()   # "2026-05-29" の形

    # --- id: 送られればそれ、無ければ生成して衝突回避 ---
    if entry.id is not None:
        new_id = entry.id
    else:
        base = f"{entry_date.strftime('%Y%m%d')}-{now.strftime('%H%M%S')}-{entry.source}"
        new_id = _make_unique_id(db, base)

    # --- hash: 送られればそれ、無ければ生成 ---
    if entry.hash is not None:
        new_hash = entry.hash
    else:
        new_hash = make_hash(new_id, date_str, entry.content)

    # --- SQLAlchemyモデルを組み立てて保存 ---
    db_entry = models.RawEntry(
        id=new_id,
        date=entry_date,
        source=entry.source,
        content=entry.content,
        hash=new_hash,
        title=entry.title,
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def search_by_keyword(db: Session, query: str, limit: int = 20, source: str = None):
    """
    本文 or タイトルに query を含む日記を、新しい順に返す。
    SQLAlchemyの .filter() と .contains() で「部分一致」を表現する。
    """
    q = db.query(models.RawEntry).filter(
        models.RawEntry.content.contains(query)
    )
    if source:
        q = q.filter(models.RawEntry.source == source)
    return q.order_by(models.RawEntry.date.desc()).limit(limit).all()


def list_by_date_range(db: Session, start: str, end: str, source: str = None):
    """
    期間で絞って古い順に返す = 仕様書「時間軸対話モード」のSQL版。
    start/end は 'YYYY-MM-DD' 形式の文字列。
    """
    q = db.query(models.RawEntry).filter(
        models.RawEntry.date >= start,
        models.RawEntry.date <= end,
    )
    if source:
        q = q.filter(models.RawEntry.source == source)
    return q.order_by(models.RawEntry.date.asc()).all()