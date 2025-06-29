import time
from asyncio import Lock
from datetime import datetime
from typing import AsyncIterable, List, Optional, Tuple

from nerdd_link.utils import ObservableList

from ..models import (
    AnonymousUser,
    Challenge,
    Job,
    JobInternal,
    JobUpdate,
    JobWithResults,
    ModuleInternal,
    Result,
    ResultCheckpoint,
    Source,
    User,
)
from ..util import CompressedSet
from .exceptions import RecordAlreadyExistsError, RecordNotFoundError
from .repository import Repository

__all__ = ["MemoryRepository"]


class MemoryRepository(Repository):
    def __init__(self) -> None:
        pass

    #
    # INITIALIZATION
    #
    async def initialize(self) -> None:
        self.transaction_lock = Lock()
        self.jobs = ObservableList[JobInternal]()
        self.modules = ObservableList[ModuleInternal]()
        self.sources = ObservableList[Source]()
        self.results = ObservableList[Result]()
        self.checkpoints = ObservableList[ResultCheckpoint]()
        self.users = ObservableList[User]()
        self.challenges = ObservableList[Challenge]()

    #
    # MODULES
    #
    async def get_module_changes(
        self,
    ) -> AsyncIterable[Tuple[Optional[ModuleInternal], Optional[ModuleInternal]]]:
        async for change in self.modules.changes():
            yield change

    async def get_all_modules(self) -> List[ModuleInternal]:
        return self.modules.get_items()

    async def create_module(self, module: ModuleInternal) -> ModuleInternal:
        assert module.id is not None
        async with self.transaction_lock:
            try:
                await self.get_module_by_id(module.id)
                raise RecordAlreadyExistsError(ModuleInternal, module.id)
            except RecordNotFoundError:
                self.modules.append(module)
                return module

    async def update_module(self, module: ModuleInternal) -> ModuleInternal:
        async with self.transaction_lock:
            existing_module = await self.get_module_by_id(module.id)
            self.modules.update(existing_module, module)
            return await self.get_module_by_id(module)

    async def get_module_by_id(self, id: str) -> ModuleInternal:
        try:
            return next((module for module in self.modules.get_items() if module.id == id))
        except StopIteration as e:
            raise RecordNotFoundError(ModuleInternal, id) from e

    #
    # JOBS
    #
    async def get_job_changes(
        self, job_id: str
    ) -> AsyncIterable[Tuple[Optional[JobInternal], Optional[JobInternal]]]:
        async for old, new in self.jobs.changes():
            if (old is not None and old.id == job_id) or (new is not None and new.id == job_id):
                yield (old, new)

    async def create_job(self, job: JobInternal) -> JobWithResults:
        async with self.transaction_lock:
            try:
                await self.get_job_by_id(job.id)
                raise RecordAlreadyExistsError(JobInternal, job.id)
            except RecordNotFoundError:
                self.jobs.append(job)
                return JobWithResults(
                    **job.model_dump(),
                    entries_processed=CompressedSet(),
                )

    async def update_job(self, job_update: JobUpdate) -> JobInternal:
        async with self.transaction_lock:
            # find job instance
            existing_job = next(
                (job for job in self.jobs.get_items() if job.id == job_update.id), None
            )
            if existing_job is None:
                raise RecordNotFoundError(JobInternal, job_update.id)

            # create a modified job instance based on the existing one
            modified_job = JobInternal(**existing_job.model_dump())
            if job_update.status is not None:
                modified_job.status = job_update.status
            if job_update.num_entries_total is not None:
                modified_job.num_entries_total = job_update.num_entries_total
            if job_update.num_checkpoints_total is not None:
                modified_job.num_checkpoints_total = job_update.num_checkpoints_total
            if job_update.new_output_formats is not None:
                modified_job.output_formats.extend(job_update.new_output_formats)

            # update the job in the observable list
            self.jobs.update(existing_job, modified_job)
            return await self.get_job_by_id(job_update.id)

    async def get_job_by_id(self, id: str) -> JobWithResults:
        # fetch all corresponding results
        results = await self.get_results_by_job_id(id)
        entries_processed = CompressedSet([result.mol_id for result in results]).to_intervals()

        try:
            return next(
                (
                    JobWithResults(**job.model_dump(), entries_processed=entries_processed)
                    for job in self.jobs.get_items()
                    if job.id == id
                )
            )
        except StopIteration as e:
            raise RecordNotFoundError(Job, id) from e

    async def delete_job_by_id(self, id: str) -> None:
        async with self.transaction_lock:
            job = await self.get_job_by_id(id)
            self.jobs.remove(job)

    async def get_expired_jobs(self, deadline: datetime) -> AsyncIterable[JobInternal]:
        for job in self.jobs.get_items():
            if job.created_at < deadline:
                yield job

    #
    # SOURCES
    #
    async def create_source(self, source: Source) -> Source:
        async with self.transaction_lock:
            try:
                await self.get_source_by_id(source.id)
                raise RecordAlreadyExistsError(Source, source.id)
            except RecordNotFoundError:
                self.sources.append(source)
                return source

    async def get_source_by_id(self, id: str) -> Source:
        try:
            return next((source for source in self.sources.get_items() if source.id == id))
        except StopIteration as e:
            raise RecordNotFoundError(Source, id) from e

    async def delete_source_by_id(self, id: str) -> None:
        async with self.transaction_lock:
            source = await self.get_source_by_id(id)
            self.sources.remove(source)

    async def get_expired_sources(self, deadline: datetime) -> AsyncIterable[Source]:
        for source in self.sources.get_items():
            if source.created_at < deadline:
                yield source

    #
    # RESULTS
    #
    async def get_result_changes(
        self,
        job_id: str,
        start_mol_id: Optional[int] = None,
        end_mol_id: Optional[int] = None,
    ) -> AsyncIterable[Tuple[Optional[Result], Optional[Result]]]:
        async for change in self.results.changes():
            old, new = change
            if (
                old is not None
                and old.job_id == job_id
                and start_mol_id <= old.mol_id <= end_mol_id
            ) or (
                new is not None
                and new.job_id == job_id
                and start_mol_id <= new.mol_id <= end_mol_id
            ):
                yield change

    async def get_result_by_id(self, id: str) -> Result:
        try:
            return next((result for result in self.results.get_items() if result.id == id))
        except StopIteration as e:
            raise RecordNotFoundError(Result, id) from e

    async def get_results_by_job_id(
        self,
        job_id: str,
        start_mol_id: Optional[int] = None,
        end_mol_id: Optional[int] = None,
    ) -> List[Result]:
        return [
            result
            for result in self.results.get_items()
            if result.job_id == job_id
            and (start_mol_id is None or start_mol_id <= result.mol_id)
            and (end_mol_id is None or result.mol_id <= end_mol_id)
        ]

    async def create_result(self, result: Result) -> None:
        async with self.transaction_lock:
            try:
                await self.get_result_by_id(result.id)
                raise RecordAlreadyExistsError(Result, result.id)
            except RecordNotFoundError:
                self.results.append(result)

    async def get_all_results_by_job_id(self, job_id: str) -> List[Result]:
        return [result for result in self.results.get_items() if result.job_id == job_id]

    async def delete_results_by_job_id(self, job_id) -> None:
        async with self.transaction_lock:
            results_to_delete = [
                result for result in self.results.get_items() if result.job_id == job_id
            ]
            for result in results_to_delete:
                self.results.remove(result)

    #
    # CHECKPOINTS
    #
    async def create_result_checkpoint(self, checkpoint: ResultCheckpoint) -> ResultCheckpoint:
        async with self.transaction_lock:
            try:
                await self.get_result_checkpoints_by_job_id(checkpoint.job_id)
                raise RecordAlreadyExistsError(ResultCheckpoint, checkpoint.job_id)
            except RecordNotFoundError:
                self.checkpoints.append(checkpoint)
                return checkpoint

    async def update_result_checkpoint(self, checkpoint: ResultCheckpoint) -> ResultCheckpoint:
        async with self.transaction_lock:
            existing_checkpoint = next(
                (cp for cp in self.checkpoints.get_items() if cp.id == checkpoint.id), None
            )
            if existing_checkpoint is None:
                raise RecordNotFoundError(ResultCheckpoint, checkpoint.id)

            self.checkpoints.update(existing_checkpoint, checkpoint)
            return await self.get_result_checkpoints_by_job_id(checkpoint.job_id)

    async def get_result_checkpoints_by_job_id(self, job_id: str) -> List[ResultCheckpoint]:
        return [
            checkpoint for checkpoint in self.checkpoints.get_items() if checkpoint.job_id == job_id
        ]

    async def get_result_checkpoints_by_module_id(self, module_id):
        return [
            checkpoint
            for checkpoint in self.checkpoints.get_items()
            if checkpoint.job_type == module_id
        ]

    async def delete_result_checkpoints_by_job_id(self, job_id: str) -> None:
        async with self.transaction_lock:
            checkpoints_to_delete = [
                checkpoint
                for checkpoint in self.checkpoints.get_items()
                if checkpoint.job_id == job_id
            ]
            for checkpoint in checkpoints_to_delete:
                self.checkpoints.remove(checkpoint)

    #
    # USERS
    #
    async def get_user_by_ip_address(self, ip_address: str) -> User:
        try:
            return next((user for user in self.users.get_items() if user.ip_address == ip_address))
        except StopIteration as e:
            raise RecordNotFoundError(User, ip_address) from e

    # Note: this method is not mandatory for the repository interface.
    async def get_user_by_id(self, id: str) -> User:
        try:
            return next((user for user in self.users.get_items() if user.id == id))
        except StopIteration as e:
            raise RecordNotFoundError(User, id) from e

    async def create_user(self, user: User) -> User:
        async with self.transaction_lock:
            try:
                await self.get_user_by_id(user.id)
                raise RecordAlreadyExistsError(User, user.id)
            except RecordNotFoundError:
                result = AnonymousUser(**user.model_dump())
                self.users.append(result)
                return result

    async def get_recent_jobs_by_user(self, user, num_seconds):
        return [
            job
            for job in self.jobs.get_items()
            if job.user_id == user.id and (job.created_at.timestamp() > (time.time() - num_seconds))
        ]

    #
    # CHALLENGES
    #
    async def get_challenge_by_salt(self, salt: str) -> Challenge:
        try:
            return next((challenge for challenge in self.challenges if challenge.salt == salt))
        except StopIteration as e:
            raise RecordNotFoundError(Challenge, salt) from e

    # Note: this method is not mandatory for the repository interface.
    async def get_challenge_by_id(self, id: str) -> User:
        try:
            return next((challenge for challenge in self.challenges if challenge.id == id))
        except StopIteration as e:
            raise RecordNotFoundError(Challenge, id) from e

    async def create_challenge(self, challenge: Challenge) -> Challenge:
        async with self.transaction_lock:
            try:
                await self.get_challenge_by_id(challenge.id)
                raise RecordAlreadyExistsError(Challenge, challenge.id)
            except RecordNotFoundError:
                self.challenges.append(challenge)
                return challenge

    async def delete_challenge_by_id(self, id: str) -> None:
        async with self.transaction_lock:
            existing_challenge = await self.get_challenge_by_id(id)
            self.challenges.remove(existing_challenge)

    async def delete_expired_challenges(self, deadline: datetime) -> None:
        async with self.transaction_lock:
            for challenge in self.challenges:
                if challenge.expires_at < deadline:
                    self.challenges.remove(challenge)
