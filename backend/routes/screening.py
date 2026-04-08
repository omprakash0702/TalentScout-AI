from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.db.database import SessionLocal
from backend.db import models
from utils.logger import logger
from utils.auth_utils import get_current_user

from backend.core.conversation import handle_conversation  

# ADDED
import re

router = APIRouter()


# Proper DB dependency (fix)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ADDED: score extraction (same logic as chat)
def extract_score(text: str):
    try:
        match = re.search(r'(\d+)\s*/\s*10', text)
        if match:
            return int(match.group(1))
    except Exception as e:
        logger.error(f"Score extraction error: {e}")
    return None


@router.post("/screen")
def screen(
    resume: str,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    logger.info(f"User {user_id} started screening")

    session = {}

    response = handle_conversation(resume, session)

    # ADDED: extract score
    score_value = extract_score(response)

    # ================= SAFE DB SAVE (IMPROVED) =================
    try:
        history = models.ScreeningHistory(
            user_id=user_id,
            resume_text=resume,
            score=score_value if score_value is not None else "N/A",
            feedback=response
        )

        db.add(history)
        db.commit()

    except Exception as e:
        db.rollback()   # ADDED safety
        logger.error(f"DB Error (screen): {e}")

    # ==========================================================

    logger.info(f"User {user_id} completed screening")

    return {
        "response": response,
        "status": "success"
    }


# HISTORY ROUTE 
@router.get("/history")
def get_history(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:
        history = db.query(models.ScreeningHistory)\
                    .filter(models.ScreeningHistory.user_id == user_id)\
                    .order_by(models.ScreeningHistory.created_at.desc())\
                    .limit(100)\
                    .all()

        # Clean response 
        return [
            {
                "resume": h.resume_text,
                "score": h.score,
                "feedback": h.feedback,
                "created_at": str(h.created_at)
            }
            for h in history
        ]

    except Exception as e:
        logger.error(f"DB Error (history): {e}")
        return []


# ADDED: CLEAR HISTORY ROUTE
@router.delete("/history")
def clear_history(
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    try:
        db.query(models.ScreeningHistory)\
          .filter(models.ScreeningHistory.user_id == user_id)\
          .delete()

        db.commit()

        return {"message": "History cleared"}

    except Exception as e:
        db.rollback()
        logger.error(f"DB Error (clear history): {e}")
        return {"message": "Error clearing history"}