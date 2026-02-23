import pytest
from nerdd_link import ResultMessage

from nerdd_backend.actions.save_result_to_db import SaveResultToDb
from nerdd_backend.models import JobInternal


@pytest.fixture
def data_dir(tmp_path):
    return str(tmp_path)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("root_path", "expected_url"),
    [
        (None, "/jobs/path-job/files/calculated-property/record-7"),
        ("/api", "/api/jobs/path-job/files/calculated-property/record-7"),
    ],
)
async def test_replaces_property_file_paths_with_urls(root_path, expected_url, client, monkeypatch):
    action = SaveResultToDb(client.app)

    # overwrite the root_path in the app's config
    monkeypatch.setattr(client.app.state.config, "root_path", root_path)

    repository = client.app.state.repository
    await repository.create_job(
        JobInternal(
            id="message-job",
            job_type="test-module",
            source_id="source-id",
            params={},
        )
    )

    #
    # valid property file path
    #
    valid_property_file_path = action.storage.get_property_file_path(
        "path-job", "calculated-property", "record-7"
    )

    await action._process_messages(
        [
            ResultMessage(
                job_id="message-job",
                mol_id=1,
                some_property=valid_property_file_path,
            )
        ]
    )

    saved_result = await repository.get_result_by_id("message-job-1")
    assert saved_result.some_property == expected_url


    #
    # invalid storage path
    #
    invalid_storage_path = action.storage.get_output_file_path("path-job", "sdf")

    await action._process_messages(
        [
            ResultMessage(
                job_id="message-job",
                mol_id=2,
                some_property=invalid_storage_path,
            )
        ]
    )

    saved_result = await repository.get_result_by_id("message-job-2")
    assert saved_result.some_property == invalid_storage_path

    #
    # not a path at all
    #
    ordinary_value="not a storage path"

    await action._process_messages(
        [
            ResultMessage(
                job_id="message-job",
                mol_id=3,
                some_property=ordinary_value,
            )
        ]
    )

    saved_result = await repository.get_result_by_id("message-job-3")
    assert saved_result.some_property == ordinary_value
