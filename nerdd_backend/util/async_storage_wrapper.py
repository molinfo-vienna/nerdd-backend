import asyncio
import json
from collections.abc import AsyncIterator
from typing import Literal

from nerdd_link import Storage
from nerdd_module.config import Module

__all__ = ["AsyncStorageWrapper"]


class AsyncStorageWrapper:
    def __init__(self, storage: Storage) -> None:
        self.storage = storage

    async def module_exists(self, module_id: str) -> bool:
        return await asyncio.to_thread(self.storage.module_file_exists, module_id)

    async def property_file_exists(self, job_id: str, property_name: str, record_id: str) -> bool:
        file_path = self.storage.get_property_file_path(job_id, property_name, record_id)
        return await asyncio.to_thread(self.storage.file_exists, file_path)

    async def output_file_exists(self, job_id: str, output_format: str) -> bool:
        return await asyncio.to_thread(self.storage.output_file_exists, job_id, output_format)

    async def delete_source_file(self, source_id: str) -> None:
        await asyncio.to_thread(self.storage.delete_source_file, source_id)

    def _iter_file_chunks(
        self,
        file_path: str,
        mode: Literal["rb"],
        *,
        chunk_size: int = 65536,
    ) -> AsyncIterator[bytes]:
        if mode != "rb":
            raise ValueError("Only binary read mode ('rb') is supported.")
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive.")

        async def _iterate() -> AsyncIterator[bytes]:
            file_handle = await asyncio.to_thread(self.storage.get_file_handle, file_path, mode)
            try:
                while chunk := await asyncio.to_thread(file_handle.read, chunk_size):
                    yield chunk
            finally:
                await asyncio.to_thread(file_handle.close)

        return _iterate()

    def iter_output_file_chunks(
        self,
        job_id: str,
        output_format: str,
        mode: Literal["rb"],
        *,
        chunk_size: int = 65536,
    ) -> AsyncIterator[bytes]:
        file_path = self.storage.get_output_file_path(job_id, output_format)
        return self._iter_file_chunks(file_path, mode, chunk_size=chunk_size)

    def iter_property_file_chunks(
        self,
        job_id: str,
        property_name: str,
        record_id: str,
        mode: Literal["rb"],
        *,
        chunk_size: int = 65536,
    ) -> AsyncIterator[bytes]:
        file_path = self.storage.get_property_file_path(job_id, property_name, record_id)
        return self._iter_file_chunks(file_path, mode, chunk_size=chunk_size)

    async def write_model_config(self, model_config: Module) -> None:

        def _write() -> None:
            with self.storage.get_module_file_handle(model_config.id, "w") as file_handle:
                json.dump(model_config.model_dump(), file_handle)

        await asyncio.to_thread(_write)

    async def load_model_config(self, module_id: str) -> Module:

        def _load() -> Module:
            with self.storage.get_module_file_handle(module_id, "r") as file_handle:
                return Module.model_validate(json.load(file_handle))

        return await asyncio.to_thread(_load)
