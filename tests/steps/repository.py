import pytest_asyncio
from pytest_bdd import given

from nerdd_backend.data import MemoryRepository


@pytest_asyncio.fixture(scope="function")
async def repository(mocker):
    return MemoryRepository()


@given("a mocked repository")
def mocked_repository(mocker, repository):
    mocker.patch(
        "nerdd_backend.main.get_repository",
        return_value=repository,
    )


# TODO move this to the correct file
# @given("the repository contains the mol weight module")
# @async_step
# async def mol_weight_module(repository):
#     model = MolWeightModel()
#     await repository.upsert_module(Module(**model.get_config().model_dump()))
