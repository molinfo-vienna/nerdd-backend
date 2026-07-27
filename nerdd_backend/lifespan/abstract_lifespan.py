from fastapi import FastAPI

__all__ = ["AbstractLifespan"]


class AbstractLifespan:
    def __init__(self) -> None:
        pass

    async def start(self, app: FastAPI) -> None:
        pass

    async def run(self) -> None:
        pass

    async def stop(self) -> None:
        pass
