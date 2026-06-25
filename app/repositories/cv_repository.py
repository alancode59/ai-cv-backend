from datetime import datetime, timezone
from app.models.mongo import get_database
from bson import ObjectId

db = get_database()
collection = db["cv_analyses"]


def save_analysis(cv_text: str, job_description: str, result: dict) -> str:
    document = {
        "cv_text": cv_text,
        "job_description": job_description,
        "result": result,
        "created_at": datetime.now(timezone.utc)
    }

    inserted = collection.insert_one(document)

    return str(inserted.inserted_id)


def get_all_analyses():
    analyses = collection.find().sort("created_at", -1)
    results = []

    for analysis in analyses:
        results.append({
            "id": str(analysis["_id"]),
            "cv_text": analysis["cv_text"],
            "job_description": analysis["job_description"],
            "score": analysis["result"]["score"],
            "skills_detectadas": analysis["result"]["skills_detectadas"],
            "skills_faltantes": analysis["result"]["skills_faltantes"],
            "recomendaciones": analysis["result"]["recomendaciones"],
            "created_at": analysis["created_at"].isoformat()
        })

    return results


def get_analysis_by_id(analysis_id: str):
    if not ObjectId.is_valid(analysis_id):
        return None

    return collection.find_one({
        "_id": ObjectId(analysis_id)
    })
