from abc import ABC, abstractmethod
from typing import Optional

from spotipyio.consts.typing_consts import Json
from spotipyio.logic.authentication.spotify_session import SpotifySession


class ISpotifyComponent(ABC):
    def __init__(self, session: SpotifySession):
        self._session = session

    @abstractmethod
    async def run(self, *args, **kwargs) -> Optional[Json]:
        raise NotImplementedError
