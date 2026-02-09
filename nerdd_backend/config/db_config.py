from dataclasses import dataclass
from typing import Optional


@dataclass
class DbConfig:
    name: str = "memory"
    host: Optional[str] = None
    port: Optional[int] = None
    database_name: Optional[str] = None
