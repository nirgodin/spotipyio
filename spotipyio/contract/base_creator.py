from abc import ABC

from spotipyio.logic.authentication.spotify_session import SpotifySession


class BaseCreator(ABC):
    def __init__(self, session: SpotifySession):
        self._session = session

    async def create(self, *args, **kwargs):  # TODO: Add output typing
        raise NotImplementedError
