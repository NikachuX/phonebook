from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routes import router
from app.database import engine, Base
import app.models

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

fatsapi_app = FastAPI()
Base.metadata.create_all(bind=engine)
fatsapi_app.include_router(router, prefix="/api")


fatsapi_app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)

@fatsapi_app.get("/", include_in_schema=False)
def index():
    return FileResponse(STATIC_DIR / "index.html")