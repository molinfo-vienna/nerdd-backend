from typing import Any, Generic, TypeVar

from fastapi import FastAPI
from nerdd_link import Action, Message, Storage, Topic

__all__ = ["ActionWithContext"]

TMessage = TypeVar("TMessage", bound=Message)


class ActionWithContext(Action[TMessage], Generic[TMessage]):
    def __init__(self, app: FastAPI, topic: Topic[TMessage], **kwargs: Any) -> None:
        super().__init__(topic, **kwargs)
        self.app: FastAPI = app
        # Do not set channel, because the superclass nerdd_link.Action already does that via
        # topic. Also, channel is a read-only property of the superclass so assigning self.channel
        # would raise an exception.
        # self.channel = app.state.channel
        self.repository = app.state.repository
        self.storage: Storage = app.state.storage
        self.config = app.state.config

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
