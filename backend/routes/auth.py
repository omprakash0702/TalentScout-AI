from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.db.database import SessionLocal
from backend.db import models
from utils.auth_utils import create_token

from passlib.context import CryptContext

router = APIRouter()

# ✅ INDUSTRY-LEVEL HASHING (Argon2)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# ✅ Request body model (clean API)
class UserAuth(BaseModel):
    email: str
    password: str


# ✅ Proper DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ================= REGISTER =================
@router.post("/register")
def register(data: UserAuth, db: Session = Depends(get_db)):

    email = data.email
    password = data.password

    # check existing user
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = pwd_context.hash(password)

    user = models.User(email=email, password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"msg": "User created"}


# ================= LOGIN =================
@router.post("/login")
def login(data: UserAuth, db: Session = Depends(get_db)):

    email = data.email
    password = data.password

    user = db.query(models.User).filter(models.User.email == email).first()

    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(user.id)

    return {"access_token": token}