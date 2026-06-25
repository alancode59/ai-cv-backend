from fastapi import APIRouter, HTTPException
from app.services.ai_service import AIServiceError

from app.schemas.cv_schema import (
    CVAnalysisRequest,
    CVAnalysisResponse
)

from app.services.cv_service import (
    analyze_cv,
    get_analysis_history,
    get_analysis_detail
)

router = APIRouter(
    prefix="/api/cv",
    tags=["CV Analysis"]
)


@router.post(
    "/analyze",
    response_model=CVAnalysisResponse
)
def analyze(data: CVAnalysisRequest):
    try:
        return analyze_cv(
            data.cv_text,
            data.job_description
        )

    except AIServiceError as error:
        raise HTTPException(
            status_code=502,
            detail=str(error)
        )


@router.get("/history")
def get_history():

    return get_analysis_history()


@router.get("/history/{analysis_id}")
def get_history_detail(analysis_id: str):

    analysis = get_analysis_detail(analysis_id)

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found"
        )

    return analysis
