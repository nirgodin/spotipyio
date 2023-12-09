from typing import Dict, Type

from spotipyio.contract.base_manager import BaseManager
from spotipyio.contract.spotify_component_interface import ISpotifyComponent
from spotipyio.logic.collectors.singles_collectors.playlists_collector import PlaylistsCollector
from spotipyio.logic.creators.playlists.playlists_creator import PlaylistsCreator
from spotipyio.logic.updaters.playlist.playlist_cover_updater import PlaylistCoverUpdater
from spotipyio.logic.updaters.playlist.playlist_items_adder import PlaylistItemsAdder


class PlaylistsManager(BaseManager):
    def __init__(self,
                 info: PlaylistsCollector,
                 create: PlaylistsCreator,
                 add_items: PlaylistItemsAdder,
                 update_cover: PlaylistCoverUpdater):
        super().__init__()
        self.info = info
        self.create = create
        self.add_items = add_items
        self.update_cover = update_cover

    @staticmethod
    def _components() -> Dict[str, Type[ISpotifyComponent]]:
        return {
            "info": PlaylistsCollector,
            "creator": PlaylistsCreator,
            "add_items": PlaylistItemsAdder,
            "update_cover": PlaylistCoverUpdater
        }
