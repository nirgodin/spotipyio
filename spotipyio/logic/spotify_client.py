from aiohttp import ClientSession

from spotipyio.logic.collectors.chunks_collectors.albums_collector import AlbumsCollector
from spotipyio.logic.collectors.chunks_collectors.artists_collector import ArtistsCollector
from spotipyio.logic.collectors.chunks_collectors.audio_features_collector import AudioFeaturesCollector
from spotipyio.logic.collectors.chunks_collectors.tracks_collector import TracksCollector
from spotipyio.logic.managers.artists_manager import ArtistsManager


class SpotifyClient:
    def __init__(self,
                 artists_manager: ArtistsManager,
                 albums_collector: AlbumsCollector,
                 tracks_collector: TracksCollector,
                 audio_features_collector: AudioFeaturesCollector):
        self.artists = artists_manager
        self.albums = albums_collector
        self.tracks = tracks_collector
        self.audio_features = audio_features_collector

    @classmethod
    def create(cls, session: ClientSession) -> "SpotifyClient":
        return SpotifyClient(
            artists_manager=ArtistsManager.create(session),
            albums_collector=AlbumsCollector(session),
            tracks_collector=TracksCollector(session),
            audio_features_collector=AudioFeaturesCollector(session)
        )
