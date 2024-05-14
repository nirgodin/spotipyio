from typing import List

from spotipyio.consts.spotify_consts import TRACKS
from spotipyio.consts.typing_consts import Json
from spotipyio.contract import BasePlaylistsUpdater


class PlaylistItemsReplacer(BasePlaylistsUpdater):
    async def run(self, playlist_id: str, uris: List[str]) -> Json:
        url = self._build_url(playlist_id)
        return await self._session.put(
            url=url,
            payload={"uris": uris}
        )

    @property
    def _route(self) -> str:
        return TRACKS
