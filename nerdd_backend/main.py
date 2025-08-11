import asyncio
import logging
import os
from contextlib import asynccontextmanager

import hydra
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from nerdd_link import FileSystem, KafkaChannel, MemoryChannel, SystemMessage
from nerdd_link.utils import async_to_sync
from omegaconf import DictConfig, OmegaConf, open_dict

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
from .data import MemoryRepository, RethinkDbRepository
from .lifespan import ActionLifespan, CreateModuleLifespan
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


def get_channel(config: DictConfig):
    if config.channel.name == "kafka":
        return KafkaChannel(config.channel.broker_url)
    elif config.channel.name == "memory":
        return MemoryChannel()
    else:
        raise ValueError(f"Unsupported channel name: {config.channel.name}")


def get_repository(config: DictConfig):
    if config.db.name == "rethinkdb":
        return RethinkDbRepository(config.db.host, config.db.port, config.db.database_name)
    elif config.db.name == "memory":
        return MemoryRepository()
    else:
        raise ValueError(f"Unsupported database: {config.db.name}")


async def create_app(cfg: DictConfig):
    lifespans = [
        ActionLifespan(lambda app: UpdateJobSize(app.state.channel, app.state.repository, cfg)),
        ActionLifespan(
            lambda app: SaveModuleToDb(
                app.state.channel, app.state.repository, app.state.filesystem
            )
        ),
        ActionLifespan(lambda app: SaveResultToDb(app.state.channel, app.state.repository)),
        ActionLifespan(
            lambda app: SaveResultCheckpointToDb(app.state.channel, app.state.repository, cfg)
        ),
        ActionLifespan(
            lambda app: StartSerialization(app.state.channel, app.state.repository, cfg)
        ),
        ActionLifespan(
            lambda app: ProcessSerializationResult(app.state.channel, app.state.repository, cfg)
        ),
        ActionLifespan(
            lambda app: TrackPredictionSpeed(app.state.channel, app.state.repository, cfg)
        ),
        ActionLifespan(lambda app: DeleteJob(app.state.channel, app.state.repository, cfg)),
        ActionLifespan(
            lambda app: DeleteExpiredResources(
                app.state.channel, app.state.repository, app.state.filesystem, cfg
            )
        ),
        CreateModuleLifespan(),
    ]

    # Set default values for configuration options if not provided
    with open_dict(cfg):
        cfg.challenge_hmac_key = getattr(cfg, "challenge_hmac_key", os.urandom(32).hex())
        cfg.challenge_difficulty = getattr(cfg, "challenge_difficulty", 1_000_000)
        cfg.challenge_expiration_seconds = getattr(cfg, "challenge_expiration_seconds", 3600)

    if cfg.mock_infra:
        from nerdd_link import (
            PredictCheckpointsAction,
            ProcessJobsAction,
            RegisterModuleAction,
            SerializeJobAction,
        )

        from .util import MolWeightModel

        model = MolWeightModel()

        lifespans = [
            *lifespans,
            ActionLifespan(
                lambda app: RegisterModuleAction(app.state.channel, model, cfg.media_root)
            ),
            ActionLifespan(
                lambda app: PredictCheckpointsAction(app.state.channel, model, cfg.media_root)
            ),
            ActionLifespan(
                lambda app: ProcessJobsAction(
                    app.state.channel,
                    num_test_entries=10,
                    ratio_valid_entries=0.5,
                    maximum_depth=100,
                    max_num_lines_mol_block=10_000,
                    data_dir=cfg.media_root,
                )
            ),
            ActionLifespan(lambda app: SerializeJobAction(app.state.channel, cfg.media_root)),
        ]

    @asynccontextmanager
    async def global_lifespan(app: FastAPI):
        logger.info("Starting tasks")
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
    app.state.repository = repository = get_repository(cfg)
    app.state.channel = channel = get_channel(cfg)
    app.state.filesystem = FileSystem(cfg.media_root)
    app.state.config = cfg

    await channel.start()

    await repository.initialize()

    if cfg.mock_infra:
        await channel.system_topic().send(SystemMessage())

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


@hydra.main(version_base=None, config_path="settings", config_name="development")
@async_to_sync
async def main(cfg: DictConfig) -> None:
    logger.info(f"Starting server with the following configuration:\n{OmegaConf.to_yaml(cfg)}")
    app = await create_app(cfg)

    config = uvicorn.Config(
        app,
        host=cfg.host,
        port=cfg.port,
        log_level="info",
        # Use the url (protocol, host) provided in the X-Forwarded-* headers. This is important,
        # because nerdd-backend runs behind a reverse proxy (traefik) and the normal request
        # headers (host, port, protocol) do not contain the correct values.
        proxy_headers=True,
        forwarded_allow_ips="*",
        # do not use root_path here, because it breaks local development (and it doesn't improve
        # a production setup either)
        # root_path=cfg.root_path,
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    main()
