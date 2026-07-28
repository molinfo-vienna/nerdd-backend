import logging

import requests
from fastapi import FastAPI
from nerdd_link import ModuleMessage

from ..data import RecordAlreadyExistsError
from ..models import ModuleInternal
from ..util import AsyncStorageWrapper
from .action_with_context import ActionWithContext

__all__ = ["SaveModuleToDb"]

logger = logging.getLogger(__name__)


class SaveModuleToDb(ActionWithContext[ModuleMessage]):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app, app.state.channel.modules_topic())

    async def _process_message(self, message: ModuleMessage) -> None:
        module_id = message.id
        logger.info(f"Creating a new module called {module_id}")

        async_storage = AsyncStorageWrapper(self.storage)
        if not await async_storage.module_exists(module_id):
            logger.error(f"Module file for {module_id} does not exist")
            return

        module_json = (await async_storage.load_model_config(module_id)).model_dump()

        # fetch publication information from doi.org
        def _f(publication: dict) -> dict:
            doi = publication.get("doi")
            if doi is None:
                logger.warning("Publication does not have a DOI")
                return publication

            logger.info(f"Fetching metadata for publication with DOI {doi}")

            headers = {"Accept": "application/vnd.citationstyles.csl+json"}

            r = requests.get(f"http://doi.org/{doi}", headers=headers, timeout=60)

            if r.status_code != 200:
                logger.warning(f"Failed to fetch metadata for DOI {doi}")
                return publication

            metadata = r.json()

            # remove large and unnecessary fields
            for field in ["abstract", "reference"]:
                if field in metadata:
                    del metadata[field]

            return metadata

        processed_publications = (
            [_f(p) for p in module_json["publications"]]
            if module_json.get("publications") is not None
            else []
        )

        new_module = ModuleInternal(**module_json, processed_publications=processed_publications)
        try:
            await self.repository.create_module(new_module)
        except RecordAlreadyExistsError:
            logger.info(f"Module with id {new_module.id} already exists in the database")
            logger.info("Updating existing module")
            # TODO: consider merging instead of overwriting
            await self.repository.update_module(new_module)

    def _get_group_name(self) -> str:
        return "save-module-to-db"
