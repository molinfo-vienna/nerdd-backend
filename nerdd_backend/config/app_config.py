from dataclasses import dataclass, field
from typing import List, Optional

from .channel_config import ChannelConfig
from .db_config import DbConfig


@dataclass
class AppConfig:
    host: str = "0.0.0.0"
    port: int = 8000
    root_path: Optional[str] = None
    log_requests: bool = True
    cors: bool = True

    quota_mols_per_day_anonymous: int = 100_000
    quota_active_jobs_anonymous: int = 5

    challenge_difficulty: int = 1_000_000
    challenge_expiration_seconds: int = 3600

    max_num_molecules_per_job: int = 10_000
    max_job_duration_minutes: int = 360
    max_checkpoint_duration_minutes: int = 5
    job_expiration_days: int = 60

    page_size_molecular_property_prediction: int = 5
    page_size_atom_property_prediction: int = 3
    page_size_derivative_property_prediction: int = 2

    media_root: str = "./media"
    mock_infra: bool = False

    output_formats: List[str] = field(default_factory=lambda: ["sdf", "csv"])

    channel: ChannelConfig = field(default_factory=ChannelConfig)
    db: DbConfig = field(default_factory=DbConfig)
