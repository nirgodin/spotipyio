from abc import ABC, abstractmethod

from spotipyio.consts.spotify_consts import SPOTIFY_API_BASE_URL, PLAYLISTS
from spotipyio.contract.spotify_component_interface import ISpotifyComponent


class BasePlaylistsUpdater(ISpotifyComponent, ABC):
    @property
    @abstractmethod
    def _route(self) -> str:
        raise NotImplementedError

    def _build_url(self, playlist_id: str) -> str:
        return f"{SPOTIFY_API_BASE_URL}/{PLAYLISTS}/{playlist_id}/{self._route}"
