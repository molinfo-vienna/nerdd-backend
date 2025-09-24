from typing import Literal

from pydantic import BaseModel

__all__ = ["QueueStats"]


class QueueStats(BaseModel):
    module_id: str
    num_active_jobs: int
    waiting_time_minutes: int
    estimate: Literal["upper_bound", "lower_bound"]
