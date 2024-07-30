from abc import ABC, abstractmethod
from functools import partial
from typing import List, Optional

from spotipyio.contract.spotify_component_interface import ISpotifyComponent
from spotipyio.logic.authentication.spotify_session import SpotifySession
from spotipyio.tools import AioPoolExecutor


class BasePaginationCollector(ISpotifyComponent, ABC):
    def __init__(self, session: SpotifySession, pool_executor: AioPoolExecutor = AioPoolExecutor()):
        super().__init__(session)
        self._pool_executor = pool_executor

    async def run(self, ids: List[str], paginate: bool = False) -> List[dict]:
        func = partial(self.run_single, paginate=paginate)
        return await self._pool_executor.run(iterable=ids, func=func, expected_type=dict)

    async def run_single(self, id_: str, paginate: bool = False) -> dict:
        url = self._url_format.format(id=id_)
        result = await self._session.get(url=url)

        if paginate:
            await self._append_additional_pages_items(result)

        return result

    async def _append_additional_pages_items(self, result: dict) -> None:
        next_url = self._extract_first_next_url(result)

        while next_url is not None:
            page = await self._session.get(url=next_url, params=self._additional_items_request_params)
            self._extend_existing_items(result, page)
            next_url = self._extract_subsequent_next_url(page)

    @property
    @abstractmethod
    def _url_format(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def _additional_items_request_params(self) -> Optional[dict]:
        raise NotImplementedError

    @abstractmethod
    def _extract_first_next_url(self, result: dict) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    def _extract_subsequent_next_url(self, page: dict) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    def _extend_existing_items(self, result: dict, page: dict) -> None:
        raise NotImplementedError
