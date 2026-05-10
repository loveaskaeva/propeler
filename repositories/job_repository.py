from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from models.job import Job
from models.enums import JobStatus
from typing import Optional, Dict, Any
import uuid

class JobRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, job_id: uuid.UUID) -> Optional[Job]:
        result = await self.session.execute(select(Job).where(Job.id == job_id))
        return result.scalar_one_or_none()

    async def update_job_result(self, job_id: uuid.UUID, result_data: Dict[str, Any]):
        await self.session.execute(
            update(Job)
            .where(Job.id == job_id)
            .values(result=result_data, status=JobStatus.DONE)
        )
        await self.session.commit()

    async def update_job_status(self, job_id: uuid.UUID, status: JobStatus, result_data: Optional[Dict[str, Any]] = None):
        values = {"status": status}
        if result_data:
            values["result"] = result_data
            
        await self.session.execute(
            update(Job)
            .where(Job.id == job_id)
            .values(**values)
        )
        await self.session.commit()
