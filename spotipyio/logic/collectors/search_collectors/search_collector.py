from typing import List

from spotipyio.contract import ISpotifyComponent
from spotipyio.logic.authentication.spotify_session import SpotifySession
from spotipyio.logic.collectors.search_collectors.search_item import SearchItem
from spotipyio.tools import PoolExecutor


class SearchCollector(ISpotifyComponent):
    def __init__(self, base_url: str, session: SpotifySession, pool_executor: PoolExecutor = PoolExecutor()):
        super().__init__(base_url=base_url, session=session)
        self._pool_executor = pool_executor

    async def run(self, search_items: List[SearchItem]) -> List[dict]:
        return await self._pool_executor.run(iterable=search_items, func=self.run_single, expected_type=dict)

    async def run_single(self, search_item: SearchItem) -> dict:
        return await self._session.get(url=self._url, params=search_item.to_query_params())

    @property
    def _route(self) -> str:
        return "search"

    @property
    def _url(self) -> str:
        return f"{self._base_url}/{self._route}"
