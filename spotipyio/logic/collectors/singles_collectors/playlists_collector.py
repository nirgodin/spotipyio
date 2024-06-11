from functools import partial
from typing import List

from spotipyio.consts.spotify_consts import SPOTIFY_API_BASE_URL, PLAYLISTS, TRACKS, NEXT, ITEMS, TRACK, \
    ADDITIONAL_TYPES
from spotipyio.contract import ISpotifyComponent
from spotipyio.logic.authentication.spotify_session import SpotifySession
from spotipyio.tools import PoolExecutor
from spotipyio.utils import safe_nested_get


class PlaylistsCollector(ISpotifyComponent):
    def __init__(self, session: SpotifySession, pool_executor: PoolExecutor = PoolExecutor()):
        super().__init__(session)
        self._pool_executor = pool_executor

    async def run(self, ids: List[str], paginate: bool = False) -> List[dict]:
        func = partial(self.run_single, paginate)
        return await self._pool_executor.run(iterable=ids, func=func, expected_type=dict)

    async def run_single(self, id_: str, paginate: bool = False) -> dict:
        url = f"{SPOTIFY_API_BASE_URL}/{PLAYLISTS}/{id_}"
        playlist = await self._session.get(url=url)

        if paginate:
            await self._append_additional_pages_items(playlist)

        return playlist

    async def _append_additional_pages_items(self, playlist: dict) -> None:
        next_url = safe_nested_get(playlist, [TRACKS, NEXT])

        while next_url is not None:
            page = await self._session.get(url=next_url, params={ADDITIONAL_TYPES: TRACK})
            existing_items: List[dict] = playlist["tracks"]["items"]
            page_items: dict = page[ITEMS]
            existing_items.extend(page_items)
            next_url = page["next"]
