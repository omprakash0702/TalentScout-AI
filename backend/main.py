from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from backend.chat import router as chat_router
from backend.routes import auth, screening
from backend.db.database import Base, engine


# ---------- APP ----------
app = FastAPI()


Base.metadata.create_all(bind=engine)
# ---------- ROUTES ----------
# existing
app.include_router(chat_router)

# new (auth + screening)
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(screening.router, tags=["Screening"])


# ---------- ROOT ----------
@app.get("/")
def home():
    return {"message": "Backend running"}