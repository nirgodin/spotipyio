from typing import List

from spotipyio.consts.spotify_consts import TRACKS, URI, SNAPSHOT_ID
from spotipyio.consts.typing_consts import Json
from spotipyio.contract import BasePlaylistsUpdater


class PlaylistItemsRemover(BasePlaylistsUpdater):
    async def run(self, playlist_id: str, uris: List[str], snapshot_id: str) -> Json:
        url = self._build_url(playlist_id)
        payload = {
            TRACKS: [{URI: uri} for uri in uris],
            SNAPSHOT_ID: snapshot_id
        }

        return await self._session.delete(
            url=url,
            payload=payload
        )

    @property
    def _route(self) -> str:
        return TRACKS
