from sqlalchemy.orm import Session
from app.db import models
from app.schemas import raw as schemas

def create_raw_entry(db: Session, entry: schemas.RawEntryCreate):
    # PydanticモデルをSQLAlchemyモデルに変換
    db_entry = models.RawEntry(**entry.model_dump())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry