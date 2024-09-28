import asyncio
from asyncio import AbstractEventLoop

from _pytest.fixtures import fixture
from pytest_httpserver import HTTPServer

from spotipyio import SpotifyClient, SpotifySession, SpotifyGrantType
from spotipyio.consts.api_consts import GRANT_TYPE, JSON, ACCESS_TOKEN
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
def base_url(test_client: SpotifyTestClient) -> str:
    return test_client.get_base_url()


@fixture(scope="session")
async def spotify_client(base_url: str, spotify_session: SpotifySession) -> SpotifyClient:
    return SpotifyClient.create(
        session=spotify_session,
        base_url=base_url
    )


@fixture(scope="session")
def authorization_server() -> HTTPServer:
    with HTTPServer() as mock_authorization_server:
        yield mock_authorization_server


@fixture(scope="session")
def token_request_url(authorization_server: HTTPServer) -> str:
    return authorization_server.url_for("").rstrip("/")


@fixture(scope="session")
async def spotify_session(authorization_server: HTTPServer, token_request_url: str) -> SpotifySession:
    authorization_server.expect_request(
        uri="/",
        method="POST",
        data=f'{GRANT_TYPE}={SpotifyGrantType.CLIENT_CREDENTIALS.value}&{JSON}=True',
    ).respond_with_json({ACCESS_TOKEN: "bla"})
    raw_session = SpotifySession(
        token_request_url=token_request_url,
        client_id="a",
        client_secret="b",
        redirect_uri="c",
    )

    async with raw_session as session:
        yield session
