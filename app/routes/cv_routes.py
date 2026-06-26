from fastapi import APIRouter, HTTPException, UploadFile, File, Form
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

from app.services.pdf_service import extract_text_from_pdf

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


@router.post(
    "/analyze-pdf",
    response_model=CVAnalysisResponse
)
async def analyze_pdf(
    cv_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    if cv_file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    file_bytes = await cv_file.read()

    cv_text = extract_text_from_pdf(file_bytes)

    if not cv_text:
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from PDF"
        )

    try:
        return analyze_cv(
            cv_text=cv_text,
            job_description=job_description
        )

    except AIServiceError as error:
        raise HTTPException(
            status_code=502,
            detail=str(error)
        )
