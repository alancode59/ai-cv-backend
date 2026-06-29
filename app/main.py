from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes.health_routes import router as health_router
from app.routes.cv_routes import router as cv_router

app = FastAPI(
    title="AI CV Analyzer API",
    description="Backend para análisis inteligente de CVs utilizando LLMs",
    version="0.0.1"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {}
    )


app.include_router(health_router)
app.include_router(cv_router)
