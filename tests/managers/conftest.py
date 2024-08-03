import asyncio
from asyncio import AbstractEventLoop

from _pytest.fixtures import fixture
from pytest_httpserver import HTTPServer

from spotipyio import SpotifyClient, SpotifySession
from spotipyio.testing import SpotifyTestClient
from spotipyio.utils import create_client_session


@fixture(scope="session")
def event_loop() -> AbstractEventLoop:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@fixture(scope="session")
def test_client() -> SpotifyTestClient:
    with HTTPServer() as mock_server:
        yield SpotifyTestClient.create(mock_server)


@fixture(scope="session")
async def spotify_client(test_client: SpotifyTestClient) -> SpotifyClient:
    raw_session = create_client_session()

    async with SpotifySession(session=raw_session) as session:
        yield SpotifyClient.create(
            session=session,
            base_url=test_client.get_base_url()
        )
