from spotipyio.contract import ISpotifyComponent
from spotipyio.logic.creators.playlists.playlists_creation_request import PlaylistCreationRequest


class PlaylistsCreator(ISpotifyComponent):
    async def run(self, request: PlaylistCreationRequest):
        url = self._url_format.format(user_id=request.user_id)
        return await self._session.post(url=url, payload=request.to_payload())

    @property
    def _url_format(self) -> str:
        return f"{self._base_url}/users/{{user_id}}/playlists"
