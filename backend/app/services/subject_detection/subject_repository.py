from app.database.connection import SessionLocal
from app.database.models import AcademicSubject

def load_subjects():

    db = SessionLocal()

    try:

        return db.query(AcademicSubject).all()

    finally:

        db.close()