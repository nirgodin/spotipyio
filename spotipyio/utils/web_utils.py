from ssl import create_default_context

from aiohttp import ClientSession, TCPConnector, CookieJar
from certifi import where


def create_client_session() -> ClientSession:
    ssl_context = create_default_context(cafile=where())
    return ClientSession(
        connector=TCPConnector(ssl=ssl_context),
        cookie_jar=CookieJar(quote_cookie=False)
    )
