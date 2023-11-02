from abc import ABC, abstractmethod
from typing import List, Union

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

    @abstractmethod
    @property
    def _route(self) -> str:
        raise NotImplementedError

    @property
    def _url(self) -> str:
        return f"{SPOTIFY_API_BASE_URL}/{self._route}"

    async def _get(self, params: dict) -> Json:
        async with self._session.get(url=self._url, params=params) as raw_response:
            raw_response.raise_for_status()  # TODO: Add more accurate error handling
            return await raw_response.json()

    async def _post(self, payload: dict) -> Json:
        async with self._session.post(url=self._url, json=payload) as raw_response:
            raw_response.raise_for_status()  # TODO: Add more accurate error handling
            return await raw_response.json()
