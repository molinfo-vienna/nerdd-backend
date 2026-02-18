import logging
from typing import Any

from fastapi import FastAPI

from .abstract_lifespan import AbstractLifespan

__all__ = ["ActionLifespan"]

logger = logging.getLogger(__name__)


class ActionLifespan(AbstractLifespan):
    def __init__(self, action_or_factory: Any) -> None:
        super().__init__()
        self.action_or_factory = action_or_factory
        self.action: Any = None

    async def start(self, app: FastAPI) -> None:
        if callable(self.action_or_factory):
            self.action = self.action_or_factory(app)
        else:
            self.action = self.action_or_factory
        logger.info(f"Start action {self.action}")

    async def run(self) -> None:
        logger.info(f"Run action {self.action}")
        await self.action.run()

    async def stop(self) -> None:
        logger.info(f"Stop action {self.action}")
        self.action = None
