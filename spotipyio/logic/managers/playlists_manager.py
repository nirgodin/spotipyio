from typing import Dict, Type

from spotipyio.contract import BaseManager, ISpotifyComponent
from spotipyio.logic.collectors.singles_collectors.playlists_collector import PlaylistsCollector
from spotipyio.logic.creators.playlists.playlists_creator import PlaylistsCreator
from spotipyio.logic.updaters.playlist.playlist_cover_updater import PlaylistCoverUpdater
from spotipyio.logic.updaters.playlist.playlist_items_adder import PlaylistItemsAdder
from spotipyio.logic.updaters.playlist.playlist_items_remover import PlaylistItemsRemover
from spotipyio.logic.updaters.playlist.playlist_items_reorder import PlaylistItemsReorder
from spotipyio.logic.updaters.playlist.playlist_items_replacer import PlaylistItemsReplacer


class PlaylistsManager(BaseManager):
    def __init__(self,
                 info: PlaylistsCollector,
                 create: PlaylistsCreator,
                 add_items: PlaylistItemsAdder,
                 update_cover: PlaylistCoverUpdater,
                 replace_items: PlaylistItemsReplacer,
                 reorder_items: PlaylistItemsReorder,
                 remove_items: PlaylistItemsRemover):
        super().__init__()
        self.info = info
        self.create = create
        self.add_items = add_items
        self.update_cover = update_cover
        self.replace_items = replace_items
        self.reorder_items = reorder_items
        self.remove_items = remove_items

    @staticmethod
    def _components() -> Dict[str, Type[ISpotifyComponent]]:
        return {
            "info": PlaylistsCollector,
            "create": PlaylistsCreator,
            "add_items": PlaylistItemsAdder,
            "update_cover": PlaylistCoverUpdater,
            "replace_items": PlaylistItemsReplacer,
            "reorder_items": PlaylistItemsReorder,
            "remove_items": PlaylistItemsRemover
        }
