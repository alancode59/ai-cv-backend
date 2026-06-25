from fastapi import FastAPI

from app.routes.health_routes import router as health_router
from app.routes.cv_routes import router as cv_router


app = FastAPI(
    title="AI CV Analyzer API",
    description="Backend para análisis inteligente de CVS utilizando LLMs",
    version="0.0.1"
)


@app.get("/")
def root():
    return {
        "message": "FastAPI funcionando"
    }


app.include_router(health_router)
app.include_router(cv_router)
