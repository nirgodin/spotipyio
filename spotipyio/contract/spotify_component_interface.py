from abc import ABC, abstractmethod
from typing import Optional

from spotipyio.consts.typing_consts import Json
from spotipyio.logic.authentication.spotify_session import SpotifySession


class ISpotifyComponent(ABC):
    def __init__(self, base_url: str, session: SpotifySession):
        self._base_url = base_url
        self._session = session

    @abstractmethod
    async def run(self, *args, **kwargs) -> Optional[Json]:
        raise NotImplementedError
