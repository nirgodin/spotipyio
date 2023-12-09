from spotipyio.consts.spotify_consts import SPOTIFY_USERS_BASE_URL
from spotipyio.contract.base_creator import BaseCreator
from spotipyio.logic.creators.playlists.playlists_creation_request import PlaylistCreationRequest


class PlaylistsCreator(BaseCreator):
    async def create(self, request: PlaylistCreationRequest):
        url = f"{SPOTIFY_USERS_BASE_URL}/{request.user_id}/playlists"
        return await self._session.post(url=url, payload=request.to_payload())
