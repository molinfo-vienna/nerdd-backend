from typing import Generic, TypeVar

from nerdd_link import Action, Storage

__all__ = ["ActionWithContext"]

TMessage = TypeVar("TMessage")


class ActionWithContext(Action[TMessage], Generic[TMessage]):
    def __init__(self, app, topic, **kwargs) -> None:
        super().__init__(topic, **kwargs)
        self.app = app
        # Do not set channel, because the superclass nerdd_link.Action already does that via
        # topic. Also, channel is a read-only property of the superclass so assigning self.channel
        # would raise an exception.
        # self.channel = app.state.channel
        self.repository = app.state.repository
        self.storage: Storage = app.state.storage
        self.config = app.state.config
