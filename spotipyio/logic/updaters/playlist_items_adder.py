from typing import List, Dict

from spotipyio.consts.spotify_consts import URIS, SPOTIFY_PLAYLISTS_BASE_URL, TRACKS
from spotipyio.contract.spotify_component_interface import ISpotifyComponent


class PlaylistItemsAdder(ISpotifyComponent):
    async def run(self, playlist_id: str, uris: List[str]) -> Dict[str, str]:
        payload = {
            URIS: ' '.join(uris)
        }
        url = f"{SPOTIFY_PLAYLISTS_BASE_URL}/{playlist_id}/{TRACKS}"

        return await self._session.post(url=url, payload=payload)
