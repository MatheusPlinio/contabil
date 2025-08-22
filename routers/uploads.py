from fastapi import APIRouter, Depends, Query
from models.upload import Upload
from sqlalchemy.orm import Session
from database.config import SessionLocal
from typing import List
from datetime import datetime

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/uploads", response_model=List[dict])
def list_uploads(
    competencia: str | None = Query(None, description="Formato: YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    query = db.query(Upload)

    if competencia:
        try:
            competencia_date = datetime.strptime(
                competencia, "%Y-%m-%d").date()
            query = query.filter(Upload.date == competencia_date)
        except ValueError:
            return {"error": "Formato inválido. Use YYYY-MM-DD"}

    uploads = query.all()
    return [
        {
            "id": u.id,
            "filename": u.filename,
            "url": u.url,
            "date": u.date.isoformat() if u.date else None,
            "created_at": u.created_at.isoformat() if u.created_at else None,
        }
        for u in uploads
    ]
