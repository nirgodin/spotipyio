from spotipyio.consts.spotify_consts import SPOTIFY_USERS_BASE_URL
from spotipyio.contract import ISpotifyComponent
from spotipyio.logic.creators.playlists.playlists_creation_request import PlaylistCreationRequest


class PlaylistsCreator(ISpotifyComponent):
    async def run(self, request: PlaylistCreationRequest):
        url = f"{SPOTIFY_USERS_BASE_URL}/{request.user_id}/playlists"
        return await self._session.post(url=url, payload=request.to_payload())
