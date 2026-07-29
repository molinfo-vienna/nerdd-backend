import pytest

from nerdd_backend.models import JobInternal, ModuleInternal
from nerdd_backend.routers.dynamic import get_dynamic_router


@pytest.fixture
def data_dir(tmp_path):
    return str(tmp_path)


async def add_module_routes_and_job(client) -> None:
    repository = client.app.state.repository
    await repository.create_job(
        JobInternal(
            id="123",
            job_type="alpha",
            source_id="source-id",
            params={},
        )
    )

    client.app.include_router(get_dynamic_router(ModuleInternal(name="alpha")))
    client.app.include_router(get_dynamic_router(ModuleInternal(name="beta")))


@pytest.mark.parametrize(
    ("method", "path"),
    [
        ("GET", "/beta/jobs/123"),
        ("DELETE", "/beta/jobs/123"),
        ("GET", "/beta/jobs/123/results"),
    ],
)
@pytest.mark.asyncio
async def test_dynamic_http_routes_reject_jobs_from_another_module(client, method, path):
    await add_module_routes_and_job(client)

    response = client.request(method, path)

    assert response.status_code == 404
    assert response.json() == {"detail": "Job not found"}


@pytest.mark.asyncio
async def test_dynamic_http_routes_allow_jobs_from_their_module(client):
    await add_module_routes_and_job(client)

    response = client.get("/alpha/jobs/123")

    assert response.status_code == 200
    assert response.json()["job_type"] == "alpha"
