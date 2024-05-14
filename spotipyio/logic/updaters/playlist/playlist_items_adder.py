from typing import List, Dict, Optional

from spotipyio.consts.spotify_consts import URIS, TRACKS
from spotipyio.contract import BasePlaylistsUpdater


class PlaylistItemsAdder(BasePlaylistsUpdater):
    async def run(self, playlist_id: str, uris: List[str], position: Optional[int] = None) -> Dict[str, str]:
        payload = {
            URIS: uris,
            "position": position
        }
        url = self._build_url(playlist_id)

        return await self._session.post(url=url, payload=payload)

    @property
    def _route(self) -> str:
        return TRACKS
