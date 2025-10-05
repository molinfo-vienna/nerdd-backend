import asyncio
import logging

from ..routers import get_dynamic_router
from .abstract_lifespan import AbstractLifespan

__all__ = ["CreateModuleLifespan"]

logger = logging.getLogger(__name__)


class CreateModuleLifespan(AbstractLifespan):
    def __init__(self):
        super().__init__()

    async def start(self, app):
        self.app = app

    async def run(self):
        logger.info("Starting CreateModuleLifespan")
        repository = self.app.state.repository

        async for old, new in repository.get_module_changes():
            try:
                if old is None:
                    module = new
                    logger.info(f"Creating module {module.name}")

                    new_router = get_dynamic_router(module)
                    paths = [route.path for route in new_router.routes]

                    # delete old routes
                    self.app.router.routes = [
                        route for route in self.app.router.routes if route.path not in paths
                    ]

                    self.app.include_router(new_router)

                    # reload the routing table
                    self.app.openapi_schema = None
            except asyncio.CancelledError:
                logger.info("Cancelled CreateModuleLifespan")
            except Exception as e:
                logger.error(e)

        logger.info("Stopping CreateModuleLifespan")
