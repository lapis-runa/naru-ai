from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import raw as schemas
from app.crud import raw as crud
from app.services import vector

router = APIRouter()

@router.post("/", response_model=schemas.RawEntryResponse)
def create_entry(entry: schemas.RawEntryCreate, db: Session = Depends(get_db)):
    return crud.create_raw_entry(db=db, entry=entry)

@router.get("/search", response_model=list[schemas.RawEntryResponse])
def search_entries(
    q: str,
    source: str = None,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    """キーワード検索。/entries/search?q=劣等感 のように呼ぶ。"""
    return crud.search_by_keyword(db, query=q, limit=limit, source=source)


@router.get("/range", response_model=list[schemas.RawEntryResponse])
def entries_in_range(
    start: str,
    end: str,
    source: str = None,
    db: Session = Depends(get_db),
):
    """期間検索。/entries/range?start=2022-01-01&end=2022-12-31 のように呼ぶ。"""
    return crud.list_by_date_range(db, start=start, end=end, source=source)



@router.get("/semantic")
def semantic_search(q: str, n: int = 5, source: str = None):
    """
    意味検索。/entries/semantic?q=孤独で惨めだった話 のように呼ぶ。
    言葉が違っても意味が近い日記を引く(bge-m3)。
    """
    return vector.search(q, n_results=n, source=source)