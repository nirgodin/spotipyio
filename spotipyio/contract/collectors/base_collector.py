from abc import ABC, abstractmethod
from typing import Optional

from spotipyio.logic.authentication.spotify_grant_type import SpotifyGrantType
from spotipyio.logic.authentication.spotify_session import SpotifySession


class BaseCollector(ABC):
    def __init__(self, session: Optional[SpotifySession] = None):
        self._session = session

    @abstractmethod
    async def collect(self, *args, **kwargs):  # TODO: Add output typing
        raise NotImplementedError

    # @abstractmethod  # TODO: Think how to do it
    # def collect_sync(self, ids: List[str]):
    #     raise NotImplementedError

    def __aenter__(self,
                   grant_type: SpotifyGrantType = SpotifyGrantType.CLIENT_CREDENTIALS,
                   access_code: Optional[str] = None) -> "BaseCollector":
        self._session = await SpotifySession().__aenter__(grant_type, access_code)
        return self

    def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._session.__aexit__(exc_type, exc_val, exc_tb)
