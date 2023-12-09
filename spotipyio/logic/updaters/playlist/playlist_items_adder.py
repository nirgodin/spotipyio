from typing import List, Dict

from spotipyio.consts.spotify_consts import URIS, TRACKS
from spotipyio.contract.updaters.base_playlist_updater import BasePlaylistsUpdater


class PlaylistItemsAdder(BasePlaylistsUpdater):
    async def run(self, playlist_id: str, uris: List[str]) -> Dict[str, str]:
        payload = {
            URIS: ' '.join(uris)
        }
        url = self._build_url(playlist_id)

        return await self._session.post(url=url, payload=payload)

    @property
    def _route(self) -> str:
        return TRACKS
