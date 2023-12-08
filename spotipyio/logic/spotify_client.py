from spotipyio.logic.authentication.spotify_session import SpotifySession
from spotipyio.logic.collectors.chunks_collectors.albums_collector import AlbumsCollector
from spotipyio.logic.collectors.chunks_collectors.audio_features_collector import AudioFeaturesCollector
from spotipyio.logic.collectors.chunks_collectors.tracks_collector import TracksCollector
from spotipyio.logic.collectors.search_collectors.search_collector import SearchCollector
from spotipyio.logic.collectors.singles_collectors.playlists_collector import PlaylistsCollector
from spotipyio.logic.managers.artists_manager import ArtistsManager
from spotipyio.logic.managers.current_user_manager import CurrentUserManager


class SpotifyClient:
    def __init__(self,
                 artists_manager: ArtistsManager,
                 current_user_manager: CurrentUserManager,
                 albums_collector: AlbumsCollector,
                 tracks_collector: TracksCollector,
                 audio_features_collector: AudioFeaturesCollector,
                 playlists_collector: PlaylistsCollector,
                 search_collector: SearchCollector):
        self.artists = artists_manager
        self.albums = albums_collector
        self.tracks = tracks_collector
        self.audio_features = audio_features_collector
        self.playlists = playlists_collector
        self.search = search_collector
        self.current_user = current_user_manager

    @classmethod
    def create(cls, session: SpotifySession) -> "SpotifyClient":
        return SpotifyClient(
            artists_manager=ArtistsManager.create(session=session),
            current_user_manager=CurrentUserManager.create(session=session),
            albums_collector=AlbumsCollector(session=session),
            tracks_collector=TracksCollector(session=session),
            audio_features_collector=AudioFeaturesCollector(session=session),
            playlists_collector=PlaylistsCollector(session=session),
            search_collector=SearchCollector(session=session),
        )
