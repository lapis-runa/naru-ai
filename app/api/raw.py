from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import raw as schemas
from app.crud import raw as crud

router = APIRouter()

@router.post("/", response_model=schemas.RawEntryResponse)
def create_entry(entry: schemas.RawEntryCreate, db: Session = Depends(get_db)):
    return crud.create_raw_entry(db=db, entry=entry)