import uuid
from typing import Dict, Any
from core.exceptions import PermanentJobError
from models.enums import JobType, JobStatus

def validate_payload(payload: Any) -> Dict[str, uuid.UUID]:
    if not payload:
        raise PermanentJobError("WORD_STATS_COMPARE requires payload")
    
    left_id = payload.get("left_job_id")
    right_id = payload.get("right_job_id")
    
    if not left_id or not right_id:
        raise PermanentJobError("WORD_STATS_COMPARE requires both left_job_id and right_job_id")
    
    try:
        left_uuid = uuid.UUID(str(left_id))
        right_uuid = uuid.UUID(str(right_id))
    except ValueError:
        raise PermanentJobError("left_job_id and right_job_id must be valid UUIDs")
    
    if left_uuid == right_uuid:
        raise PermanentJobError("left_job_id and right_job_id must be different")
    
    return {"left_job_id": left_uuid, "right_job_id": right_uuid}

def compare_word_stats(left_job: Any, right_job: Any) -> Dict[str, Any]:
    # Проверка left_job
    _validate_source_job(left_job, "Left")
    # Проверка right_job
    _validate_source_job(right_job, "Right")
    
    left_words_dict = left_job.result.get("top_words", {})
    right_words_dict = right_job.result.get("top_words", {})
    
    left_words = set(left_words_dict.keys())
    right_words = set(right_words_dict.keys())
    
    common = sorted(list(left_words & right_words))
    left_only = sorted(list(left_words - right_words))
    right_only = sorted(list(right_words - left_words))
    
    return {
        "left_job_id": str(left_job.id),
        "right_job_id": str(right_job.id),
        "left_url": left_job.payload.get("url") if left_job.payload else None,
        "right_url": right_job.payload.get("url") if right_job.payload else None,
        "common_words": common,
        "left_only": left_only,
        "right_only": right_only
    }

def _validate_source_job(job: Any, side: str):
    if not job:
        raise PermanentJobError(f"{side} source job not found")
    
    if job.type != JobType.WORD_STATS:
        raise PermanentJobError(f"{side} job must be of type WORD_STATS")
    
    if job.status != JobStatus.DONE:
        raise PermanentJobError(f"{side} job must be in DONE status")
    
    if not isinstance(job.result, dict):
        raise PermanentJobError(f"{side} job result must be a dictionary")
    
    if "top_words" not in job.result or not isinstance(job.result["top_words"], dict):
        raise PermanentJobError(f"{side} job result must contain top_words dictionary")
