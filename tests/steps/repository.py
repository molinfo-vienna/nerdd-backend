import asyncio

import pytest_asyncio
from nerdd_link.tests import async_step
from pytest_bdd import given, parsers, when

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


@when(parsers.parse("the module '{module_id}' becomes available"))
@async_step
async def wait_for_module(client, module_id):
    repository = client.app.state.repository

    try:
        async with asyncio.timeout(5):
            async for _, module in repository.get_module_changes():
                if module is not None and module.id == module_id:
                    return
    except TimeoutError:
        raise AssertionError(
            f"Module {module_id!r} was not registered within 5 seconds."
        ) from None
