import asyncio
import logging
from collections.abc import Awaitable, Callable

__all__ = ["run_forever"]

logger = logging.getLogger(__name__)


async def run_forever(
    factory: Callable[[], Awaitable[object]],
    *,
    restart_delay: float = 60.0,
    label: str | None = None,
) -> None:
    worker_label = label or "<unnamed>"

    while True:
        try:
            await factory()
        except asyncio.CancelledError:
            logger.info("Cancelled worker %s", worker_label)
            raise
        except Exception:
            logger.exception("Worker %s failed", worker_label)
        else:
            logger.error("Worker %s stopped unexpectedly", worker_label)

        await asyncio.sleep(restart_delay)
