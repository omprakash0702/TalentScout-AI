from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.core.conversation import handle_conversation
from sqlalchemy.orm import Session
from backend.db.database import SessionLocal
from backend.db import models
from utils.auth_utils import get_current_user
import re

router = APIRouter()

# temporary in-memory session
session_store = {}


# ---------------------------
# REQUEST MODEL (UNCHANGED)
# ---------------------------
class ChatRequest(BaseModel):
    user_id: str
    message: str
    resume_data: dict | None = None


# ---------------------------
# DB DEPENDENCY (UNCHANGED)
# ---------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------
# NEW:SCORE EXTRACTION
# ---------------------------
def extract_score(text: str):
    try:
        match = re.search(r'(\d+)\s*/\s*10', text)
        if match:
            return int(match.group(1))
    except:
        pass
    return None


# ---------------------------
# CHAT ROUTE (UPGRADED)
# ---------------------------
@router.post("/chat")
def chat(
    req: ChatRequest,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    session_id = req.user_id
    message = req.message

    # ---------------------------
    # SESSION INIT
    # ---------------------------
    if session_id not in session_store:
        session_store[session_id] = {
            "state": "greeting",
            "messages": [],
            "candidate_data": {},
            "resume_processed": False,
        }

    session = session_store[session_id]

    # ---------------------------
    # RESUME INJECTION (UNCHANGED)
    # ---------------------------
    if req.resume_data and not session.get("resume_processed"):

        parsed = req.resume_data

        session["candidate_data"].update({
            "Full Name": parsed.get("Full Name", ""),
            "Email Address": parsed.get("Email Address", ""),
            "Job Role": parsed.get("Job Role", ""),
            "Years of Experience": parsed.get("Years of Experience", "0"),
        })

        session["tech_stack"] = parsed.get("Skills", "")
        session["projects"] = parsed.get("Projects", [])

        session["mode"] = "resume"
        session["resume_processed"] = True

    # ---------------------------
    # CALL CORE ENGINE (UNCHANGED)
    # ---------------------------
    response = handle_conversation(message, session)

    # ---------------------------
    # SCORE EXTRACTION
    # ---------------------------
    score_value = extract_score(response)

    # ---------------------------
    # SAVE TO DB (UPGRADED)
    # ---------------------------
    try:
        history = models.ScreeningHistory(
            user_id=user_id,
            resume_text=str(req.resume_data) if req.resume_data else "N/A",
            score=score_value if score_value is not None else "N/A",
            feedback=response
        )

        db.add(history)
        db.commit()

    except Exception as e:
        print("DB Save Error:", e)

    return {"response": response}