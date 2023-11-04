from abc import ABC, abstractmethod
from typing import List, Union, Optional

from aiohttp import ClientSession

from spotipyio.consts.spotify_consts import SPOTIFY_API_BASE_URL
from spotipyio.consts.typing_consts import Json


class BaseCollector(ABC):
    def __init__(self, session: ClientSession):
        self._session = session

    @abstractmethod
    async def collect(self, ids: List[str]):  # TODO: Add output typing
        raise NotImplementedError

    # @abstractmethod  # TODO: Think how to do it
    # def collect_sync(self, ids: List[str]):
    #     raise NotImplementedError

    async def _get(self, url: str, params: Optional[dict] = None) -> Json:
        async with self._session.get(url=url, params=params) as raw_response:
            raw_response.raise_for_status()  # TODO: Add more accurate error handling
            return await raw_response.json()

    async def _post(self, url: str, payload: dict) -> Json:
        async with self._session.post(url=url, json=payload) as raw_response:
            raw_response.raise_for_status()  # TODO: Add more accurate error handling
            return await raw_response.json()
