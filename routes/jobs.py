from fastapi import APIRouter, Depends, HTTPException
from typing import List
from models.job import Job
from models.enums import JobType
import uuid

router = APIRouter(tags=["Jobs"])

@router.post("/jobs", status_code=201)
async def create_job(job_type: JobType, payload: dict = None):
    # Логика создания задачи в БД и отправки в Celery
    return {"job_id": str(uuid.uuid4()), "status": "PENDING"}

@router.get("/jobs/{job_id}")
async def get_job(job_id: uuid.UUID):
    # Логика получения статуса задачи
    return {"id": str(job_id), "status": "DONE"}
