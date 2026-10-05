from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .database import init_db
from .routes import router


app = FastAPI(

    title="FitBuddy API",

    description=
        "AI Fitness Plan Generator using Gemini Models",

    version="1.0.0"
)


app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


app.include_router(router)


@app.on_event("startup")
def startup():

    init_db()