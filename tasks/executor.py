from models.enums import JobType
from tasks.handlers import word_stats_compare
from core.exceptions import PermanentJobError
import logging

logger = logging.getLogger(__name__)

class JobExecutor:
    def __init__(self, repository):
        self.repository = repository

    async def execute(self, job_id):
        job = await self.repository.get_by_id(job_id)
        if not job:
            logger.error(f"Job {job_id} not found")
            return

        try:
            if job.type == JobType.WORD_STATS_COMPARE:
                # 1 & 2: Валидация payload
                validated_ids = word_stats_compare.validate_payload(job.payload)
                
                # 3: Выгрузка задач из БД
                left_job = await self.repository.get_by_id(validated_ids["left_job_id"])
                right_job = await self.repository.get_by_id(validated_ids["right_job_id"])
                
                # 4 & 5: Сравнение и валидация исходных задач
                comparison_result = word_stats_compare.compare_word_stats(left_job, right_job)
                
                # 6: Сохранение результата
                await self.repository.update_job_result(job_id, comparison_result)
            
            # Другие типы задач...
            
        except PermanentJobError as e:
            logger.warning(f"Permanent error in job {job_id}: {e.message}")
            await self.repository.update_job_status(job_id, "FAILED", {"error": e.message})
        except Exception as e:
            logger.exception(f"Unexpected error in job {job_id}")
            await self.repository.update_job_status(job_id, "FAILED", {"error": str(e)})
