import asyncio
from asyncio import AbstractEventLoop

from _pytest.fixtures import fixture

from spotipyio import SpotifyClient
from spotipyio.logic.utils import random_alphanumeric_string
from spotipyio.testing import SpotifyTestClient
from tests.testing_utils import random_localhost_url


@fixture(scope="session")
def event_loop() -> AbstractEventLoop:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@fixture(scope="session")
async def test_client(client_id: str, client_secret: str, redirect_uri: str) -> SpotifyTestClient:
    async with SpotifyTestClient() as test_client:
        yield test_client


@fixture(scope="session")
def base_url(test_client: SpotifyTestClient) -> str:
    return test_client.get_base_url()


@fixture(scope="session")
async def spotify_client(test_client: SpotifyTestClient) -> SpotifyClient:
    client = await test_client.create_client()
    yield client
    await client.stop()


@fixture(scope="session")
def redirect_uri() -> str:
    return random_localhost_url()


@fixture(scope="session")
def client_id() -> str:
    return random_alphanumeric_string(32, 32)


@fixture(scope="session")
def client_secret() -> str:
    return random_alphanumeric_string(32, 32)
