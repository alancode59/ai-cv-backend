from fastapi import APIRouter
from app.services.ai_service import test_connection, list_models
from app.models.mongo import get_database

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("/")
def health():
    return {
        "status": "OK"
    }


@router.get("/db")
def db_health():

    db = get_database()

    db.command("ping")

    return {
        "mongo": "connected"
    }


@router.get("/ai")
def ai_health():

    response = test_connection()

    return {
        "response": response
    }


@router.get("/ai/models")
def ai_models():

    return list_models()
