import asyncio
import json
import logging
from ast import literal_eval

import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi.testclient import TestClient
from hydra import compose, initialize
from nerdd_link.tests import async_step
from pytest_bdd import parsers, then, when

from nerdd_backend.main import create_app

logger = logging.getLogger(__name__)


@pytest_asyncio.fixture
async def client(data_dir):
    # load correct config file
    with initialize(version_base=None, config_path="../../nerdd_backend/config"):
        cfg = compose(config_name="testing")

    cfg.media_root = data_dir

    # create app
    app = await create_app(cfg)

    # run app
    async with LifespanManager(app):
        client = TestClient(app)
        yield client


@when(
    parsers.parse("the client sends a POST request to {url} with content\n{data}"),
    target_fixture="response",
)
def post_request(client, url, data):
    response = client.post(url, json=json.loads(data))
    logger.info("response: %s", response.json())
    return response


@when(
    parsers.parse("the client sends a PUT request to {url} with the files"),
    target_fixture="response",
)
def put_request_with_files(client, url, files):
    actual_files = {"file": (file_name, open(file_name, "rb")) for file_name in files}
    response = client.put(url, files=actual_files)
    logger.info("response: %s", response.json())
    return response


@when(parsers.parse("the client requests {url}"), target_fixture="response")
def response(client, url):
    response = client.get(url)
    return response


@then(parsers.parse("the status code of the response is {expected_status_code:d}"))
def check_status_code(response, expected_status_code):
    status_code = response.status_code
    assert status_code == expected_status_code


@then(parsers.parse("the client receives a response with content\n{expected_response}"))
def check_response(response, expected_response):
    decoded = json.loads(expected_response)
    assert response.json() == decoded, f"Expected {decoded}, got {response.json()}"


@then(parsers.parse("the client receives a response containing\n{expected_response}"))
def check_response_contains(response, expected_response):
    decoded = literal_eval(expected_response)

    response_json = response.json()

    if isinstance(response_json, list):
        assert any(
            all(key in item and item[key] == value for key, value in decoded.items())
            for item in response_json
        ), f"Expected {decoded}, got {response.json()}"
    else:
        assert all(
            key in response.json() and response.json()[key] == value
            for key, value in decoded.items()
        ), f"Expected {decoded}, got {response.json()}"


@then(parsers.parse("the client receives a response of length {expected_length:d}"))
def check_response_length(response, expected_length):
    assert len(response.json()) == expected_length, f"Expected {expected_length}, got {response.json()}"


@when(parsers.parse("we wait for {seconds:d} seconds"))
@async_step
async def wait_for_seconds(seconds):
    await asyncio.sleep(seconds)
