from pydantic import BaseModel


class CVAnalysisRequest(BaseModel):
    cv_text: str
    job_description: str


class CVAnalysisResponse(BaseModel):
    score: int
    skills_detectadas: list[str]
    skills_faltantes: list[str]
    recomendaciones: list[str]
