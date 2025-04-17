import asyncio
import logging
from contextlib import asynccontextmanager

import hydra
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from nerdd_link import FileSystem, KafkaChannel, MemoryChannel, SystemMessage
from nerdd_link.utils import async_to_sync
from omegaconf import DictConfig, OmegaConf

from .actions import (
    ProcessSerializationResult,
    SaveModuleToDb,
    SaveResultCheckpointToDb,
    SaveResultToDb,
    UpdateJobSize,
)
from .data import MemoryRepository, RethinkDbRepository
from .lifespan import ActionLifespan, CreateModuleLifespan
from .routers import (
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
            lambda app: ProcessSerializationResult(app.state.channel, app.state.repository)
        ),
        CreateModuleLifespan(),
    ]

    if cfg.mock_infra:
        from nerdd_link import (
            PredictCheckpointsAction,
            ProcessJobsAction,
            RegisterModuleAction,
            SerializeJobAction,
        )
        from nerdd_module.tests import MolWeightModel

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
                    checkpoint_size=100,
                    max_num_molecules=10_000,
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
        # TODO: run tasks sequentially, because there might be dependencies
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

    app = FastAPI(lifespan=global_lifespan)
    app.state.repository = repository = get_repository(cfg)
    app.state.channel = channel = get_channel(cfg)
    app.state.filesystem = FileSystem(cfg.media_root)
    app.state.config = cfg

    await channel.start()

    await repository.initialize()

    if cfg.mock_infra:
        await channel.system_topic().send(SystemMessage())

    origins = [
        "http://localhost",
        "http://localhost:8000",
        "http://localhost:3000",
        "http://dev-nerdd.univie.ac.at",
        "https://dev-nerdd.univie.ac.at",
        "http://nerdd.univie.ac.at",
        "https://nerdd.univie.ac.at",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(GZipMiddleware)

    app.include_router(jobs_router)
    app.include_router(sources_router)
    app.include_router(results_router)
    app.include_router(modules_router)
    app.include_router(websockets_router)
    app.include_router(files_router)

    for module in await repository.get_all_modules():
        app.include_router(get_dynamic_router(module))

    return app


@hydra.main(version_base=None, config_path="settings", config_name="development")
@async_to_sync
async def main(cfg: DictConfig) -> None:
    logger.info(f"Starting server with the following configuration:\n{OmegaConf.to_yaml(cfg)}")
    app = await create_app(cfg)

    config = uvicorn.Config(app, host=cfg.host, port=cfg.port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    main()
