from typing import Type, Dict

from spotipyio.contract.base_manager import BaseManager
from spotipyio.contract.spotify_component_interface import ISpotifyComponent
from spotipyio.logic.collectors.chunks_collectors.artists_collector import ArtistsCollector
from spotipyio.logic.collectors.singles_collectors.artists_top_tracks_collector import ArtistsTopTracksCollector


class ArtistsManager(BaseManager):
    def __init__(self, info: ArtistsCollector, top_tracks: ArtistsTopTracksCollector):
        super().__init__()
        self.info = info
        self.top_tracks = top_tracks

    @staticmethod
    def _components() -> Dict[str, Type[ISpotifyComponent]]:
        return {
            "info": ArtistsCollector,
            "top_tracks": ArtistsTopTracksCollector
        }
