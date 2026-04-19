from dataclasses import dataclass
from typing import Optional


@dataclass
class ChannelConfig:
    name: str = "memory"
    broker_url: Optional[str] = None
    broker_username: Optional[str] = None
    broker_password: Optional[str] = None
