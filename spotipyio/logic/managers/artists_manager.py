from typing import Type, Dict

from spotipyio.contract.base_manager import BaseManager
from spotipyio.contract.collectors.base_collector import BaseCollector
from spotipyio.logic.collectors.chunks_collectors.artists_collector import ArtistsCollector
from spotipyio.logic.collectors.singles_collectors.artists_top_tracks_collector import ArtistsTopTracksCollector


class ArtistsManager(BaseManager):
    @staticmethod
    def _collectors() -> Dict[str, Type[BaseCollector]]:
        return {
            "info": ArtistsCollector,
            "top_tracks": ArtistsTopTracksCollector
        }
