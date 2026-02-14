import io
import json

import pytest
from nerdd_link import FileSystemStorage
from nerdd_module.config import Module

from nerdd_backend.util import AsyncStorageWrapper


@pytest.mark.asyncio
async def test_module_exists_returns_storage_result(tmp_path):
    storage = FileSystemStorage(str(tmp_path))
    with storage.get_module_file_handle("test-module", "w") as file_handle:
        file_handle.write("module config")

    assert await AsyncStorageWrapper(storage).module_exists("test-module")


@pytest.mark.asyncio
async def test_property_file_exists_returns_storage_result(tmp_path):
    storage = FileSystemStorage(str(tmp_path))
    with storage.get_property_file_handle("job", "property", "record", "wb") as file_handle:
        file_handle.write(b"property value")

    assert await AsyncStorageWrapper(storage).property_file_exists("job", "property", "record")


@pytest.mark.asyncio
async def test_iter_property_file_chunks_uses_property_path(tmp_path):
    storage = FileSystemStorage(str(tmp_path))
    with storage.get_property_file_handle("job", "property", "record", "wb") as file_handle:
        file_handle.write(b"abcdef")

    chunks = [
        chunk
        async for chunk in AsyncStorageWrapper(storage).iter_property_file_chunks(
            "job", "property", "record", "rb", chunk_size=3
        )
    ]

    assert chunks == [b"abc", b"def"]


@pytest.mark.asyncio
async def test_output_file_exists_returns_storage_result(tmp_path):
    storage = FileSystemStorage(str(tmp_path))
    with storage.get_output_file_handle("job", "sdf", "wb") as file_handle:
        file_handle.write(b"output value")

    assert await AsyncStorageWrapper(storage).output_file_exists("job", "sdf")


@pytest.mark.asyncio
async def test_iter_output_file_chunks_uses_output_path(tmp_path):
    storage = FileSystemStorage(str(tmp_path))
    with storage.get_output_file_handle("job", "sdf", "wb") as file_handle:
        file_handle.write(b"abcdef")

    chunks = [
        chunk
        async for chunk in AsyncStorageWrapper(storage).iter_output_file_chunks(
            "job", "sdf", "rb", chunk_size=3
        )
    ]

    assert chunks == [b"abc", b"def"]


@pytest.mark.asyncio
async def test_delete_source_file_delegates_to_storage(tmp_path):
    storage = FileSystemStorage(str(tmp_path))
    with storage.get_source_file_handle("source-id", "wb") as file_handle:
        file_handle.write(b"source value")

    await AsyncStorageWrapper(storage).delete_source_file("source-id")

    assert not storage.source_file_exists("source-id")


@pytest.mark.asyncio
async def test_iter_file_chunks_yields_binary_chunks_and_closes_handle(tmp_path):
    storage = FileSystemStorage(str(tmp_path))
    file_path = storage.get_source_file_path("source-id")
    with storage.get_file_handle(file_path, "wb") as file_handle:
        file_handle.write(b"abcdefgh")

    chunks = [
        chunk
        async for chunk in AsyncStorageWrapper(storage)._iter_file_chunks(
            file_path, "rb", chunk_size=3
        )
    ]

    assert chunks == [b"abc", b"def", b"gh"]


@pytest.mark.asyncio
async def test_iter_file_chunks_closes_handle_when_iteration_stops_early(tmp_path, monkeypatch):
    storage = FileSystemStorage(str(tmp_path))
    file_path = storage.get_source_file_path("source-id")
    with storage.get_file_handle(file_path, "wb") as file_handle:
        file_handle.write(b"abcdefgh")

    handle = storage.get_file_handle(file_path, "rb")
    monkeypatch.setattr(storage, "get_file_handle", lambda path, mode: handle)
    iterator = AsyncStorageWrapper(storage)._iter_file_chunks(file_path, "rb", chunk_size=3)

    assert await anext(iterator) == b"abc"
    await iterator.aclose()

    assert handle.closed


@pytest.mark.asyncio
async def test_iter_file_chunks_closes_handle_when_read_fails(tmp_path, monkeypatch):
    class ReadFailingHandle(io.BytesIO):
        def read(self, size=-1):
            raise OSError("read failed")

    storage = FileSystemStorage(str(tmp_path))
    handle = ReadFailingHandle(b"abcdefgh")
    file_path = storage.get_source_file_path("source-id")

    def get_failing_file_handle(path, mode):
        assert (path, mode) == (file_path, "rb")
        return handle

    monkeypatch.setattr(storage, "get_file_handle", get_failing_file_handle)

    with pytest.raises(OSError, match="read failed"):
        async_storage = AsyncStorageWrapper(storage)
        async for _ in async_storage._iter_file_chunks(file_path, "rb"):
            pass

    assert handle.closed


def test_iter_file_chunks_rejects_unsupported_modes(tmp_path):
    storage = FileSystemStorage(str(tmp_path))

    with pytest.raises(ValueError, match="Only binary read mode"):
        AsyncStorageWrapper(storage)._iter_file_chunks("file://file", "r")


def test_iter_file_chunks_rejects_non_positive_chunk_size(tmp_path):
    storage = FileSystemStorage(str(tmp_path))

    with pytest.raises(ValueError, match="chunk_size must be positive"):
        AsyncStorageWrapper(storage)._iter_file_chunks(
            "file://file", "rb", chunk_size=0
        )


@pytest.mark.asyncio
async def test_write_model_config_writes_json_and_closes_handle(tmp_path):
    config = Module(name="Test Model")
    storage = FileSystemStorage(str(tmp_path))

    await AsyncStorageWrapper(storage).write_model_config(config)

    with storage.get_module_file_handle(config.id, "r") as file_handle:
        assert json.load(file_handle) == config.model_dump()


@pytest.mark.asyncio
async def test_load_model_config_reads_json_and_closes_handle(tmp_path):
    config = Module(name="Test Model")
    storage = FileSystemStorage(str(tmp_path))
    with storage.get_module_file_handle(config.id, "w") as file_handle:
        json.dump(config.model_dump(), file_handle)

    loaded_config = await AsyncStorageWrapper(storage).load_model_config(config.id)

    assert loaded_config == config
