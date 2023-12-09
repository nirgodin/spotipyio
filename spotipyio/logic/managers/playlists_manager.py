from typing import Dict, Type

from spotipyio.contract.base_manager import BaseManager
from spotipyio.contract.collectors.base_collector import BaseCollector
from spotipyio.logic.collectors.singles_collectors.playlists_collector import PlaylistsCollector


class PlaylistsManager(BaseManager):
    def __init__(self, info: PlaylistsCollector):
        super().__init__()
        self.info = info

    @staticmethod
    def _collectors() -> Dict[str, Type[BaseCollector]]:
        return {
            "info": PlaylistsCollector,
        }
