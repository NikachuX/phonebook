from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from routes import router
from database import engine, Base
import models

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(router, prefix="/api")


app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)

@app.get("/", include_in_schema=False)
def index():
    return FileResponse(STATIC_DIR / "index.html")