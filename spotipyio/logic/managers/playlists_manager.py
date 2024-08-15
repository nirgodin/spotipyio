from typing import Dict, Type

from spotipyio.contract import BaseManager, ISpotifyComponent
from spotipyio.logic.collectors import PlaylistsCollector
from spotipyio.logic.creators.playlists.playlists_creator import PlaylistsCreator
from spotipyio.logic.updaters.playlist.playlist_cover_updater import PlaylistCoverUpdater
from spotipyio.logic.updaters.playlist.playlist_items_adder import PlaylistItemsAdder
from spotipyio.logic.updaters.playlist.playlist_items_remover import PlaylistItemsRemover
from spotipyio.logic.updaters.playlist.playlist_items_reorder import PlaylistItemsReorder
from spotipyio.logic.updaters.playlist.playlist_items_replacer import PlaylistItemsReplacer


class PlaylistsManager(BaseManager):
    def __init__(self,
                 add_items: PlaylistItemsAdder,
                 create: PlaylistsCreator,
                 info: PlaylistsCollector,
                 remove_items: PlaylistItemsRemover,
                 reorder_items: PlaylistItemsReorder,
                 replace_items: PlaylistItemsReplacer,
                 update_cover: PlaylistCoverUpdater):
        super().__init__()
        self.add_items = add_items
        self.create = create
        self.info = info
        self.remove_items = remove_items
        self.replace_items = replace_items
        self.reorder_items = reorder_items
        self.update_cover = update_cover

    @staticmethod
    def _components() -> Dict[str, Type[ISpotifyComponent]]:
        return {
            "add_items": PlaylistItemsAdder,
            "create": PlaylistsCreator,
            "info": PlaylistsCollector,
            "remove_items": PlaylistItemsRemover,
            "replace_items": PlaylistItemsReplacer,
            "reorder_items": PlaylistItemsReorder,
            "update_cover": PlaylistCoverUpdater,
        }
