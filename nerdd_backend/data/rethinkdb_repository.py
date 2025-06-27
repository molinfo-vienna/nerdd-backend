import logging
from datetime import datetime
from typing import AsyncIterable, List, Optional, Tuple

from rethinkdb import RethinkDB
from rethinkdb.errors import ReqlOpFailedError

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
    UserType,
)
from .exceptions import RecordAlreadyExistsError, RecordNotFoundError
from .repository import Repository

__all__ = ["RethinkDbRepository"]

logger = logging.getLogger(__name__)


class RethinkDbRepository(Repository):
    def __init__(self, host: str, port: int, database_name: str) -> None:
        self.r = RethinkDB()
        self.r.set_loop_type("asyncio")

        self.host = host
        self.port = port
        self.database_name = database_name

    #
    # INITIALIZATION
    #
    async def initialize(self) -> None:
        self.connection = await self.r.connect(self.host, self.port)

        # create database
        try:
            await self.r.db_create(self.database_name).run(self.connection)
        except ReqlOpFailedError as e:
            if not str(e).startswith("Database `nerdd` already exists"):
                logger.exception("Failed to create database", exc_info=e)

        # use the same database for all queries
        self.connection.use(self.database_name)

        # create tables
        await self.create_module_table()
        await self.create_sources_table()
        await self.create_jobs_table()
        await self.create_results_table()
        await self.create_result_checkpoints_table()
        await self.create_users_table()
        await self.create_challenges_table()

        # create an index on job_id in results table
        try:
            await self.r.table("results").index_create("job_id").run(self.connection)

            # wait for index to be ready
            await self.r.table("results").index_wait("job_id").run(self.connection)
        except ReqlOpFailedError as e:
            if not str(e).startswith("Index `job_id` already exists"):
                logger.exception("Failed to create index", exc_info=e)

        # create an index on job_id in checkpoints table
        try:
            await self.r.table("checkpoints").index_create("job_id").run(self.connection)

            # wait for index to be ready
            await self.r.table("checkpoints").index_wait("job_id").run(self.connection)
        except ReqlOpFailedError as e:
            if not str(e).startswith("Index `job_id` already exists"):
                logger.exception("Failed to create index", exc_info=e)

        # create an index on ip_address in anonymous_users table
        try:
            await self.r.table("users").index_create("ip_address").run(self.connection)

            # wait for index to be ready
            await self.r.table("users").index_wait("ip_address").run(self.connection)
        except ReqlOpFailedError as e:
            if not str(e).startswith("Index `ip_address` already exists"):
                logger.exception("Failed to create index", exc_info=e)

    #
    # MODULES
    #
    async def get_module_changes(
        self,
    ) -> AsyncIterable[Tuple[Optional[ModuleInternal], Optional[ModuleInternal]]]:
        cursor = await self.r.table("modules").changes(include_initial=True).run(self.connection)

        async for change in cursor:
            if "old_val" not in change or change["old_val"] is None:
                old_module = None
            else:
                old_module = ModuleInternal(**change["old_val"])

            if "new_val" not in change or change["new_val"] is None:
                new_module = None
            else:
                new_module = ModuleInternal(**change["new_val"])

            yield old_module, new_module

    async def get_all_modules(self) -> List[ModuleInternal]:
        cursor = await self.r.table("modules").run(self.connection)
        return [ModuleInternal(**item) async for item in cursor]

    async def get_module_by_id(self, module_id: str) -> ModuleInternal:
        result = await self.r.table("modules").get(module_id).run(self.connection)

        if result is None:
            raise RecordNotFoundError(ModuleInternal, module_id)

        return ModuleInternal(**result)

    async def create_module_table(self) -> None:
        try:
            await self.r.table_create("modules", primary_key="id").run(self.connection)
        except ReqlOpFailedError:
            pass

    async def create_module(self, module: ModuleInternal) -> ModuleInternal:
        result = await (
            self.r.table("modules")
            .insert(module.model_dump(), conflict="error", return_changes=True)
            .run(self.connection)
        )

        if len(result["changes"]) == 0:
            raise RecordAlreadyExistsError(ModuleInternal, module.id)

        return ModuleInternal(**result["changes"][0]["new_val"])

    async def update_module(self, module: ModuleInternal) -> ModuleInternal:
        result = await (
            self.r.table("modules")
            .get(module.id)
            .update(module.model_dump(), return_changes=True)
            .run(self.connection)
        )

        if result["skipped"] == 1:
            raise RecordNotFoundError(ModuleInternal, module.id)

        return module

    #
    # JOBS
    #
    async def get_job_changes(
        self, job_id: str
    ) -> AsyncIterable[Tuple[Optional[JobWithResults], Optional[JobInternal]]]:
        cursor = (
            await self.r.table("jobs")
            .get(job_id)
            .changes(include_initial=False)
            .run(self.connection)
        )

        async for change in cursor:
            if change["old_val"] is None:
                old_job = None
            else:
                old_job = JobInternal(**change["old_val"])

            if change["new_val"] is None:
                new_job = None
            else:
                new_job = JobInternal(**change["new_val"])

            yield old_job, new_job

    async def create_jobs_table(self) -> None:
        try:
            await self.r.table_create("jobs", primary_key="id").run(self.connection)
        except ReqlOpFailedError:
            pass

    async def create_job(self, job: JobInternal) -> JobWithResults:
        result = await (
            self.r.table("jobs")
            .insert(job.model_dump(), conflict="error", return_changes=True)
            .run(self.connection)
        )
        # JobWithResults adds the entries_processed field, which is not part of JobInternal.
        return JobWithResults(**result["changes"][0]["new_val"])

    async def update_job(self, job_update: JobUpdate) -> JobInternal:
        # all fields can be updated in a single query
        # --> prepare an object with all fields that should be updated
        update_set = {}
        if job_update.status is not None:
            update_set["status"] = job_update.status
        if job_update.num_entries_total is not None:
            update_set["num_entries_total"] = job_update.num_entries_total
        if job_update.num_checkpoints_total is not None:
            update_set["num_checkpoints_total"] = job_update.num_checkpoints_total
        if job_update.new_output_formats is not None:
            update_set["output_formats"] = self.r.row["output_formats"].set_union(
                job_update.new_output_formats
            )

        # update the job in the database
        changes = (
            await self.r.table("jobs")
            .get(job_update.id)
            .update(update_set, return_changes="always")
            .run(self.connection)
        )

        updated_job = changes["changes"][0]["new_val"] if len(changes["changes"]) > 0 else None

        if updated_job is None:
            raise RecordNotFoundError(Job, job_update.id)

        return JobInternal(**updated_job)

    async def get_job_by_id(self, job_id: str) -> JobWithResults:
        result = (
            await self.r.table("jobs")
            .get(job_id)
            .do(
                lambda job: self.r.branch(
                    job.eq(None),  # check if job exists
                    None,
                    job.merge(
                        {
                            "entries_processed": self.r.table("results")
                            .get_all(job["id"], index="job_id")["mol_id"]
                            .coerce_to("array")
                        }
                    ),
                )
            )
            .run(self.connection)
        )

        if result is None:
            raise RecordNotFoundError(Job, job_id)

        return JobWithResults(**result)

    async def delete_job_by_id(self, job_id: str) -> None:
        await self.r.table("jobs").get(job_id).delete().run(self.connection)

    async def get_expired_jobs(self, deadline: datetime) -> AsyncIterable[JobInternal]:
        cursor = (
            await self.r.table("jobs")
            .filter(lambda job: job["expires_at"] < deadline)
            .run(self.connection)
        )

        async for item in cursor:
            yield JobInternal(**item)

    #
    # SOURCES
    #
    async def create_sources_table(self) -> None:
        try:
            await self.r.table_create("sources", primary_key="id").run(self.connection)
        except ReqlOpFailedError:
            pass

    async def create_source(self, source: Source) -> Source:
        result = await (
            self.r.table("sources")
            .insert(source.model_dump(), conflict="error", return_changes=True)
            .run(self.connection)
        )

        if len(result["changes"]) == 0:
            raise RecordNotFoundError(Source, source.id)

        return Source(**result["changes"][0]["new_val"])

    async def get_source_by_id(self, source_id: str) -> Source:
        result = await self.r.table("sources").get(source_id).run(self.connection)

        if result is None:
            raise RecordNotFoundError(Source, source_id)

        return Source(**result)

    async def delete_source_by_id(self, source_id: str) -> None:
        await self.r.table("sources").get(source_id).delete().run(self.connection)

    async def get_expired_sources(self, deadline: datetime) -> AsyncIterable[Source]:
        cursor = (
            await self.r.table("sources")
            .filter(lambda source: source["created_at"] < deadline)
            .run(self.connection)
        )

        async for item in cursor:
            yield Source(**item)

    #
    # RESULTS
    #
    async def create_results_table(self) -> None:
        try:
            await self.r.table_create("results", primary_key="id").run(self.connection)
        except ReqlOpFailedError:
            pass

    async def get_all_results_by_job_id(self, job_id: str) -> List[Result]:
        cursor = await self.r.table("results").get_all(job_id, index="job_id").run(self.connection)
        return [Result(**item) async for item in cursor]

    async def get_results_by_job_id(
        self,
        job_id: str,
        start_mol_id: Optional[int] = None,
        end_mol_id: Optional[int] = None,
    ) -> List[Result]:
        start_condition = (
            (self.r.row["mol_id"] >= start_mol_id) if start_mol_id is not None else True
        )
        end_condition = (self.r.row["mol_id"] <= end_mol_id) if end_mol_id is not None else True

        cursor = (
            await self.r.table("results")
            .get_all(job_id, index="job_id")
            .filter(start_condition & end_condition)
            .order_by("mol_id")
            .run(self.connection)
        )

        if cursor is None:
            raise RecordNotFoundError(Result, job_id)

        return [Result(**item) for item in cursor]

    async def create_result(self, result: Result) -> Result:
        # TODO: return result
        await (
            self.r.table("results")
            .insert(result.model_dump(), conflict="error")
            .run(self.connection)
        )

    async def get_result_changes(
        self,
        job_id: str,
        start_mol_id: Optional[int] = None,
        end_mol_id: Optional[int] = None,
    ) -> AsyncIterable[Tuple[Optional[Result], Optional[Result]]]:
        start_condition = (
            (self.r.row["mol_id"] >= start_mol_id) if start_mol_id is not None else True
        )
        end_condition = (self.r.row["mol_id"] <= end_mol_id) if end_mol_id is not None else True

        cursor = (
            await self.r.table("results")
            .get_all(job_id, index="job_id")
            .filter(start_condition & end_condition)
            .changes(include_initial=True)
            .run(self.connection)
        )

        async for change in cursor:
            if "old_val" not in change or change["old_val"] is None:
                old_result = None
            else:
                old_result = Result(**change["old_val"])

            if "new_val" not in change or change["new_val"] is None:
                new_result = None
            else:
                new_result = Result(**change["new_val"])

            yield old_result, new_result

    async def delete_results_by_job_id(self, job_id: str) -> None:
        await self.r.table("results").get_all(job_id, index="job_id").delete().run(self.connection)

    #
    # CHECKPOINTS
    #
    async def create_result_checkpoints_table(self) -> None:
        try:
            await self.r.table_create("checkpoints", primary_key="id").run(self.connection)
        except ReqlOpFailedError:
            pass

    async def create_result_checkpoint(self, checkpoint: ResultCheckpoint) -> ResultCheckpoint:
        result = await (
            self.r.table("checkpoints")
            .insert(checkpoint.model_dump(), conflict="error", return_changes=True)
            .run(self.connection)
        )

        if len(result["changes"]) == 0:
            raise RecordAlreadyExistsError(ResultCheckpoint, checkpoint.id)

        return ResultCheckpoint(**result["changes"][0]["new_val"])

    async def get_result_checkpoints_by_job_id(self, job_id: str) -> List[ResultCheckpoint]:
        cursor = (
            await self.r.table("checkpoints").get_all(job_id, index="job_id").run(self.connection)
        )
        return [ResultCheckpoint(**item) async for item in cursor]

    async def delete_result_checkpoints_by_job_id(self, job_id: str) -> None:
        await (
            self.r.table("checkpoints")
            .get_all(job_id, index="job_id")
            .delete()
            .run(self.connection)
        )

    #
    # USERS
    #
    async def create_users_table(self) -> None:
        try:
            await self.r.table_create("users", primary_key="id").run(self.connection)
        except ReqlOpFailedError:
            pass

    async def get_user_by_ip_address(self, ip_address: str) -> AnonymousUser:
        result = (
            await self.r.table("users")
            .filter(lambda user: user["ip_address"] == ip_address)
            .run(self.connection)
        )

        if result is None:
            raise RecordNotFoundError(AnonymousUser, ip_address)

        users = [AnonymousUser(**item) async for item in result]
        if len(users) == 0:
            raise RecordNotFoundError(AnonymousUser, ip_address)

        return users[0]

    async def get_user_by_id(self, user_id: str) -> User:
        result = await self.r.table("users").get(user_id).run(self.connection)

        if result is None:
            raise RecordNotFoundError(User, user_id)

        if result["user_type"] == UserType.ANONYMOUS:
            return AnonymousUser(**result)
        else:
            raise ValueError(f"Unknown user type: {result['user_type']}")

    async def create_user(self, user: User) -> User:
        result = await (
            self.r.table("users")
            .insert(user.model_dump(), conflict="error", return_changes=True)
            .run(self.connection)
        )

        if len(result["changes"]) == 0:
            raise RecordAlreadyExistsError(User, user.id)

        return user

    async def get_recent_jobs_by_user(self, user, num_seconds):
        cursor = (
            await self.r.table("jobs")
            .filter(
                lambda job: job["user_id"] == user.id
                and job["created_at"] > self.r.now().sub(num_seconds)
            )
            .order_by(self.r.desc("created_at"))
            .run(self.connection)
        )

        return [JobInternal(**item) for item in cursor]

    #
    # CHALLENGES
    #
    async def create_challenges_table(self) -> None:
        try:
            await self.r.table_create("challenges", primary_key="id").run(self.connection)
        except ReqlOpFailedError:
            pass

    async def create_challenge(self, challenge: Challenge) -> Challenge:
        result = await (
            self.r.table("challenges")
            .insert(challenge.model_dump(), conflict="error", return_changes=True)
            .run(self.connection)
        )

        if len(result["changes"]) == 0:
            raise RecordAlreadyExistsError(Challenge, challenge.id)

        return Challenge(**result["changes"][0]["new_val"])

    async def get_challenge_by_salt(self, salt: str) -> Challenge:
        result = (
            await self.r.table("challenges")
            .filter(lambda challenge: challenge["salt"] == salt)
            .run(self.connection)
        )

        if result is None:
            raise RecordNotFoundError(Challenge, salt)

        challenges = [Challenge(**item) async for item in result]
        if len(challenges) == 0:
            raise RecordNotFoundError(Challenge, salt)

        return challenges[0]

    async def delete_challenge_by_id(self, id: str) -> None:
        result = await self.r.table("challenges").get(id).delete().run(self.connection)

        if result["deleted"] == 0:
            raise RecordNotFoundError(Challenge, id)

    async def delete_expired_challenges(self, deadline: datetime) -> None:
        await (
            self.r.table("challenges")
            .filter(lambda challenge: challenge["expires_at"] < deadline)
            .delete()
            .run(self.connection)
        )
