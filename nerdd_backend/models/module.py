from typing import List, Optional

from nerdd_module.config import Module as NerddModule
from pydantic import BaseModel

__all__ = ["Module", "ModulePublic", "ModuleShort"]


class Module(NerddModule):
    pass


class ModulePublic(Module):
    module_url: str
    output_formats: List[str]


class ModuleShort(BaseModel):
    id: str
    rank: Optional[int] = None
    name: Optional[str] = None
    version: Optional[str] = None
    visible_name: Optional[str] = None
    logo: Optional[str] = None
    logo_title: Optional[str] = None
    logo_caption: Optional[str] = None
    module_url: str
    output_formats: List[str]
