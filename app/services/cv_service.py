from app.repositories.cv_repository import (
    save_analysis,
    get_all_analyses,
    get_analysis_by_id
)

from app.services.ai_service import analyze_cv_with_ai


def analyze_cv(cv_text: str, job_description: str):
    result = analyze_cv_with_ai(
        cv_text=cv_text,
        job_description=job_description
    )

    save_analysis(
        cv_text=cv_text,
        job_description=job_description,
        result=result
    )

    return result


def get_analysis_history():
    return get_all_analyses()


def get_analysis_detail(analysis_id: str):
    analysis = get_analysis_by_id(analysis_id)

    if not analysis:
        return None

    return {
        "id": str(analysis["_id"]),
        "cv_text": analysis["cv_text"],
        "job_description": analysis["job_description"],
        "score": analysis["result"]["score"],
        "skills_detectadas": analysis["result"]["skills_detectadas"],
        "skills_faltantes": analysis["result"]["skills_faltantes"],
        "recomendaciones": analysis["result"]["recomendaciones"],
        "created_at": analysis["created_at"].isoformat()
    }
