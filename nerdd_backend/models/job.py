from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, computed_field

from ..util import CompressedSet

__all__ = [
    "Job",
    "JobCreate",
    "JobPublic",
    "JobUpdate",
    "JobInternal",
    "JobWithResults",
    "OutputFile",
]

# Purpose of the different Job models:
# * JobCreate: Contains all fields required to create a new job (used in the jobs router).
# * Job: The base model containing essential fields for JobInternal, JobWithResults and JobPublic.
# * JobInternal: Contains all fields that should be stored in the database.
# * JobWithResults: Extends JobInternal with fields associated with job results.
# * JobPublic: Contains all fields that should be visible to the user.
# * JobUpdate: Specifies possible modifications to change a job record.


class OutputFile(BaseModel):
    format: str
    url: str


class Job(BaseModel):
    id: str
    job_type: str
    source_id: str
    params: dict
    created_at: datetime = datetime.now(timezone.utc)
    page_size: int = 10
    status: str
    num_entries_total: Optional[int] = None


class JobInternal(Job):
    user_id: Optional[str] = None
    referer: Optional[str] = None
    checkpoints_processed: List[int] = []
    num_checkpoints_total: Optional[int] = None
    output_formats: List[str] = []


class JobWithResults(JobInternal):
    entries_processed: CompressedSet = CompressedSet()

    @computed_field
    @property
    def num_entries_processed(self) -> int:
        return self.entries_processed.count()


class JobCreate(BaseModel):
    job_type: str
    source_id: str
    params: Dict[str, Any]


class JobPublic(Job):
    entries_processed: CompressedSet = CompressedSet()
    num_pages_total: Optional[int]
    num_pages_processed: int
    output_files: List[OutputFile]
    job_url: str
    results_url: str

    @computed_field
    @property
    def num_entries_processed(self) -> int:
        return self.entries_processed.count()


class JobUpdate(BaseModel):
    id: str
    status: Optional[str] = None
    num_entries_total: Optional[int] = None
    num_checkpoints_total: Optional[int] = None
    # checkpoint list update
    new_checkpoints_processed: Optional[List[int]] = None
    # output formats update
    new_output_formats: Optional[List[str]] = None
