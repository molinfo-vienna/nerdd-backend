from typing import List, Optional

from nerdd_module.config import Module as NerddModule
from pydantic import BaseModel

__all__ = ["Module", "ModuleInternal", "ModulePublic", "ModuleShort"]


class Module(NerddModule):
    pass


class ModuleInternal(Module):
    seconds_per_molecule: float = 30
    # estimated time the module takes to start up before processing a *batch*
    startup_time_seconds: float = 5


# We intentionally do not inherit from ModuleInternal here, to give the chance to hide internal
# fields in the future if needed.
class ModulePublic(Module):
    seconds_per_molecule: float
    startup_time_seconds: float
    max_num_molecules: int
    checkpoint_size: int
    module_url: str
    output_formats: List[str]


class ModuleShort(BaseModel):
    id: str
    rank: Optional[int] = None
    name: Optional[str] = None
    version: Optional[str] = None
    visible_name: Optional[str] = None
    logo_title: Optional[str] = None
    logo_caption: Optional[str] = None
    module_url: str
    output_formats: List[str]
