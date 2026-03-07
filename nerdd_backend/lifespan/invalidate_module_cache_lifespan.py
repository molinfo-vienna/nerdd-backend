import asyncio
import logging

from fastapi import FastAPI
from inhouse import MemoryStore

from ..routers.modules import augment_module
from .abstract_lifespan import AbstractLifespan

__all__ = ["InvalidateModuleCacheLifespan"]

logger = logging.getLogger(__name__)


class InvalidateModuleCacheLifespan(AbstractLifespan):
    """Invalidate cached module responses when the repository changes."""

    async def start(self, app: FastAPI) -> None:
        self.app = app

    async def run(self) -> None:
        logger.info("Starting InvalidateModuleCacheLifespan")
        repository = self.app.state.repository
        cache: MemoryStore = self.app.state.cache_store

        try:
            async for old, new in repository.get_module_changes():
                if (
                    old is not None
                    and new is not None
                    and augment_module(None, old) == augment_module(None, new)
                ):
                    continue

                logger.info("Module change detected")

                keys = {"modules"}
                if old is not None:
                    keys.add(f"module:{old.id}")
                if new is not None:
                    keys.add(f"module:{new.id}")
                for key in keys:
                    cache.delete(key)
        except asyncio.CancelledError:
            logger.info("Cancelled InvalidateModuleCacheLifespan")
            raise
