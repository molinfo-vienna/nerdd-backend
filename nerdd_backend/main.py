import asyncio
import logging
import os
from contextlib import asynccontextmanager
from typing import List

import hydra
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from hydra.core.config_store import ConfigStore
from nerdd_link import FileSystem, KafkaChannel, MemoryChannel, ModuleMessage
from nerdd_link.utils import async_to_sync
from omegaconf import OmegaConf, open_dict

from .actions import (
    DeleteExpiredResources,
    DeleteJob,
    ProcessSerializationResult,
    SaveModuleToDb,
    SaveResultCheckpointToDb,
    SaveResultToDb,
    StartSerialization,
    TrackPredictionSpeed,
    UpdateJobSize,
)
from .config import AppConfig, ChannelConfig, DbConfig
from .data import MemoryRepository, RethinkDbRepository
from .lifespan import AbstractLifespan, ActionLifespan, CreateModuleLifespan
from .routers import (
    challenges_router,
    files_router,
    get_dynamic_router,
    jobs_router,
    modules_router,
    results_router,
    sources_router,
    websockets_router,
)

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

cs = ConfigStore.instance()
cs.store(name="config", node=AppConfig)


def get_channel(config: ChannelConfig):
    if config.name == "kafka":
        return KafkaChannel(config.broker_url)
    elif config.name == "memory":
        return MemoryChannel()
    else:
        raise ValueError(f"Unsupported channel name: {config.name}")


def get_repository(config: DbConfig):
    if config.name == "rethinkdb":
        return RethinkDbRepository(config.host, config.port, config.database_name)
    elif config.name == "memory":
        return MemoryRepository()
    else:
        raise ValueError(f"Unsupported database: {config.name}")


async def create_app(cfg: AppConfig):
    # Set default values for configuration options if not provided
    with open_dict(cfg):
        cfg.challenge_hmac_key = getattr(cfg, "challenge_hmac_key", os.urandom(32).hex())
        cfg.challenge_difficulty = getattr(cfg, "challenge_difficulty", 1_000_000)
        cfg.challenge_expiration_seconds = getattr(cfg, "challenge_expiration_seconds", 3600)

    model = None
    if cfg.mock_infra:
        from nerdd_link import (
            PredictCheckpointsAction,
            ProcessJobsAction,
            SerializeJobAction,
        )

        from .util import MolWeightModel

        model = MolWeightModel()

    @asynccontextmanager
    async def global_lifespan(app: FastAPI):
        logger.info("Starting tasks")
        # note: lifespans is defined later and that is fine, because this function is not called
        # until the end of the main function
        start_tasks = asyncio.gather(
            *[asyncio.create_task(lifespan.start(app)) for lifespan in lifespans]
        )

        await start_tasks

        logger.info("Running tasks")
        run_tasks = asyncio.gather(*[asyncio.create_task(lifespan.run()) for lifespan in lifespans])

        yield

        logger.info("Attempting to cancel all tasks")
        run_tasks.cancel()

        try:
            await run_tasks
        except asyncio.CancelledError:
            logger.info("Tasks successfully cancelled")

    app = FastAPI(lifespan=global_lifespan, root_path=cfg.root_path)
    app.state.repository = repository = get_repository(cfg.db)
    app.state.channel = channel = get_channel(cfg.channel)
    app.state.filesystem = FileSystem(cfg.media_root)
    app.state.config = cfg

    await channel.start()

    await repository.initialize()

    lifespans: List[AbstractLifespan] = [
        ActionLifespan(UpdateJobSize),
        ActionLifespan(SaveModuleToDb),
        ActionLifespan(SaveResultToDb),
        ActionLifespan(SaveResultCheckpointToDb),
        ActionLifespan(StartSerialization),
        ActionLifespan(ProcessSerializationResult),
        ActionLifespan(TrackPredictionSpeed),
        ActionLifespan(DeleteJob),
        ActionLifespan(DeleteExpiredResources),
        CreateModuleLifespan(),
    ]

    if cfg.mock_infra:
        lifespans = [
            *lifespans,
            ActionLifespan(PredictCheckpointsAction(app.state.channel, model, cfg.media_root)),
            ActionLifespan(
                ProcessJobsAction(
                    app.state.channel,
                    num_test_entries=10,
                    ratio_valid_entries=0.5,
                    maximum_depth=100,
                    max_num_lines_mol_block=10_000,
                    data_dir=cfg.media_root,
                )
            ),
            ActionLifespan(SerializeJobAction(app.state.channel, cfg.media_root)),
        ]

    if cfg.mock_infra:
        import json

        module_id = model.config.id
        path = app.state.filesystem.get_module_file_path(module_id)
        json.dump(model.config.model_dump(), open(path, "w"))
        await channel.modules_topic().send(ModuleMessage(id=module_id))

    #
    # Middlewares
    #
    if cfg.log_requests:
        from .util import LogRequestsMiddleware

        app.add_middleware(LogRequestsMiddleware)

    if cfg.cors:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.add_middleware(GZipMiddleware)

    #
    # Routers
    #
    app.include_router(jobs_router)
    app.include_router(sources_router)
    app.include_router(results_router)
    app.include_router(modules_router)
    app.include_router(websockets_router)
    app.include_router(files_router)
    app.include_router(challenges_router)

    for module in await repository.get_all_modules():
        app.include_router(get_dynamic_router(module))

    return app


@hydra.main(version_base=None, config_path="config", config_name="development")
@async_to_sync
async def main(cfg: AppConfig) -> None:
    logger.info(f"Starting server with the following configuration:\n{OmegaConf.to_yaml(cfg)}")
    app = await create_app(cfg)

    config = uvicorn.Config(
        app,
        host=cfg.host,
        port=cfg.port,
        log_level="info",
        # Use the url (protocol, host) provided in the X-Forwarded-* headers. This is important
        # when nerdd-backend runs behind a reverse proxy (e.g. traefik, haproxy, etc.) and the
        # normal request headers (host, port, protocol) do not contain the correct values.
        proxy_headers=True,
        forwarded_allow_ips="*",
        # Do not use root_path here, because it breaks local development (and it doesn't improve
        # the production setup either).
        # root_path=cfg.root_path,
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    main()
