from app.database.connection import SessionLocal
from app.database.models import User

from app.auth.auth_service import hash_password

db = SessionLocal()

user = User(

    name="Admin",

    email="admin@academic.com",

    password=hash_password("admin123"),

    role="Admin"

)

db.add(user)

db.commit()

db.close()

print("Admin Created")