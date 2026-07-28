import asyncio
import importlib
import logging

import pytest

from nerdd_backend.util import run_forever

run_forever_module = importlib.import_module("nerdd_backend.util.run_forever")


@pytest.mark.asyncio
async def test_run_forever_retries_after_an_exception():
    attempts = 0
    second_attempt_started = asyncio.Event()
    keep_running = asyncio.Event()

    async def worker() -> None:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise RuntimeError("failed")
        second_attempt_started.set()
        await keep_running.wait()

    task = asyncio.create_task(run_forever(worker, restart_delay=0))
    await second_attempt_started.wait()
    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await task

    assert attempts == 2


@pytest.mark.asyncio
async def test_run_forever_retries_after_normal_completion():
    attempts = 0
    second_attempt_started = asyncio.Event()
    keep_running = asyncio.Event()

    async def worker() -> None:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            return
        second_attempt_started.set()
        await keep_running.wait()

    task = asyncio.create_task(run_forever(worker, restart_delay=0))
    await second_attempt_started.wait()
    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await task

    assert attempts == 2


@pytest.mark.asyncio
async def test_run_forever_waits_for_the_configured_restart_delay(monkeypatch):
    delays = []
    sleep_started = asyncio.Event()

    async def sleep(delay):
        delays.append(delay)
        sleep_started.set()
        await asyncio.Event().wait()

    async def worker() -> None:
        return

    monkeypatch.setattr(run_forever_module.asyncio, "sleep", sleep)
    task = asyncio.create_task(run_forever(worker, restart_delay=12.5))
    await sleep_started.wait()
    task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await task

    assert delays == [12.5]


@pytest.mark.asyncio
async def test_run_forever_uses_default_and_custom_labels(caplog):
    async def worker() -> None:
        raise RuntimeError("failed")

    with caplog.at_level(logging.ERROR):
        default_task = asyncio.create_task(run_forever(worker, restart_delay=60))
        await asyncio.sleep(0)
        default_task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await default_task

        custom_task = asyncio.create_task(run_forever(worker, restart_delay=60, label="modules"))
        await asyncio.sleep(0)
        custom_task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await custom_task

    assert "<unnamed>" in caplog.text
    assert "modules" in caplog.text
