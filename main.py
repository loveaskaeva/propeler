from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.database import Base, engine
from app.routers import services, contacts
from app.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Propeler API", version="1.0.0", description="API для проекта Propeler")

app.include_router(services.router)
app.include_router(contacts.router)

app.mount("/static", StaticFiles(directory="."), name="static")


@app.get("/", tags=["frontend"])
def index():
    return FileResponse("index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)
