from nerdd_link import KafkaChannel
from nerdd_link.tests import DummyChannel
from omegaconf import DictConfig

from ..data import MemoryRepository, RethinkDbRepository
from .abstract_lifespan import AbstractLifespan


class InitializeAppLifespan(AbstractLifespan):
    def __init__(self, config: DictConfig):
        super().__init__()
        self.config = config

    async def start(self, app):
        channel = self.get_channel(self.config)
        repository = self.get_repository(self.config)

        app.state.repository = repository
        app.state.channel = channel
        app.state.config = self.config

        await repository.initialize()

    def get_channel(self, config: DictConfig):
        if config.channel.name == "kafka":
            return KafkaChannel(config.channel.broker_url)
        elif config.channel.name == "memory":
            return DummyChannel()
        else:
            raise ValueError(f"Unsupported channel name: {config.channel.name}")

    def get_repository(self, config: DictConfig):
        if config.db.name == "rethinkdb":
            return RethinkDbRepository(
                config.db.host, config.db.port, config.db.database_name
            )
        elif config.db.name == "memory":
            return MemoryRepository()
        else:
            raise ValueError(f"Unsupported database: {config.db.name}")
