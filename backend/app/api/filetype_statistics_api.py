from fastapi import APIRouter
from sqlalchemy import func

from app.database.connection import SessionLocal
from app.database.models import Chunk

router = APIRouter()

@router.get("/statistics/filetypes")
def filetype_statistics():

    db = SessionLocal()

    try:

        results = (
            db.query(
                Chunk.file_type,
                func.count(
                    Chunk.id
                ).label("count")
            )
            .group_by(
                Chunk.file_type
            )
            .all()
        )

        return [
            {
                "file_type": row[0],
                "count": row[1]
            }
            for row in results
        ]

    finally:
        db.close()