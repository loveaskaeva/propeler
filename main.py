from fastapi import FastAPI
from routes import jobs

app = FastAPI(title="Job Processing System")

app.include_router(jobs.router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
