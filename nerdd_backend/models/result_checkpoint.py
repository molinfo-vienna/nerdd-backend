from typing import Optional

from pydantic import BaseModel


class ResultCheckpoint(BaseModel):
    job_id: str
    checkpoint_id: int
    elapsed_time_seconds: Optional[int] = None
