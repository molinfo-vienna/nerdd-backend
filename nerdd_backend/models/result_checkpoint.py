from typing import Optional

from pydantic import BaseModel

__all__ = ["ResultCheckpoint"]


class ResultCheckpoint(BaseModel):
    id: str
    job_id: str
    # job_type seems redundant with job_id, but we need it for the case where the job is deleted
    # and we still want to retrieve all checkpoints based on job_type
    job_type: Optional[str] = None
    checkpoint_id: int
    elapsed_time_seconds: Optional[int] = None
