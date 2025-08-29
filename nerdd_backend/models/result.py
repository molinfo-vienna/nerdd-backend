import math
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, model_validator

from .job import JobPublic

__all__ = ["Result", "Pagination", "ResultSet"]


class Result(BaseModel):
    id: str
    job_id: str
    mol_id: int

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="before")
    def sanitize_floats(cls, values):
        # convert nan values to None so that they are serialized to proper json
        def fix(v):
            if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
                return None
            return v

        return {k: fix(v) for k, v in values.items()}


class Pagination(BaseModel):
    page: int  # 1-based!
    page_size: int
    is_incomplete: bool
    first_mol_id_on_page: int
    last_mol_id_on_page: int
    previous_url: Optional[str]
    next_url: Optional[str]


class ResultSet(BaseModel):
    data: List[Result]
    job: JobPublic
    pagination: Pagination
