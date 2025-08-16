import json
import logging
import os

from nerdd_link import Action, Channel, FileSystem, ModuleMessage

from ..data import RecordAlreadyExistsError, Repository
from ..models import ModuleInternal

__all__ = ["SaveModuleToDb"]

logger = logging.getLogger(__name__)


class SaveModuleToDb(Action[ModuleMessage]):
    def __init__(self, channel: Channel, repository: Repository, filesystem: FileSystem) -> None:
        super().__init__(channel.modules_topic())
        self._repository = repository
        self._filesystem = filesystem

    async def _process_message(self, message: ModuleMessage) -> None:
        module_id = message.id
        logger.info(f"Creating a new module called {module_id}")

        # load json config from file
        module_path = self._filesystem.get_module_file_path(module_id)

        if not os.path.exists(module_path):
            logger.error(f"Module file {module_path} does not exist")
            return

        with open(module_path, "r") as f:
            module_json = json.load(f)

        new_module = ModuleInternal(**module_json)
        try:
            await self._repository.create_module(new_module)
        except RecordAlreadyExistsError:
            logger.info(f"Module with id {new_module.id} already exists in the database")
            logger.info("Updating existing module")
            # TODO: consider merging instead of overwriting
            await self._repository.update_module(new_module)

    def _get_group_name(self):
        return "save-module-to-db"
