from typing import Dict, Type

from spotipyio.contract.base_manager import BaseManager
from spotipyio.contract.spotify_component_interface import ISpotifyComponent
from spotipyio.logic.collectors.singles_collectors.playlists_collector import PlaylistsCollector
from spotipyio.logic.creators.playlists.playlists_creator import PlaylistsCreator


class PlaylistsManager(BaseManager):
    def __init__(self, info: PlaylistsCollector, creator: PlaylistsCreator):
        super().__init__()
        self.info = info
        self.creator = creator

    @staticmethod
    def _components() -> Dict[str, Type[ISpotifyComponent]]:
        return {
            "info": PlaylistsCollector,
            "creator": PlaylistsCreator
        }
