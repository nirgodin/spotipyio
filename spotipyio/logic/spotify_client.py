from spotipyio.logic.authentication.spotify_session import SpotifySession
from spotipyio.logic.collectors.chunks_collectors.albums_collector import AlbumsCollector
from spotipyio.logic.collectors.chunks_collectors.audio_features_collector import AudioFeaturesCollector
from spotipyio.logic.collectors.chunks_collectors.tracks_collector import TracksCollector
from spotipyio.logic.collectors.search_collectors.search_collector import SearchCollector
from spotipyio.logic.managers import *


class SpotifyClient:
    def __init__(self,
                 artists_manager: ArtistsManager,
                 current_user_manager: CurrentUserManager,
                 playlists_manager: PlaylistsManager,
                 users_manager: UsersManager,
                 albums_collector: AlbumsCollector,
                 tracks_collector: TracksCollector,
                 audio_features_collector: AudioFeaturesCollector,
                 search_collector: SearchCollector):
        self.artists = artists_manager
        self.albums = albums_collector
        self.tracks = tracks_collector
        self.users = users_manager
        self.audio_features = audio_features_collector
        self.playlists = playlists_manager
        self.search = search_collector
        self.current_user = current_user_manager

    @classmethod
    def create(cls, session: SpotifySession) -> "SpotifyClient":
        return SpotifyClient(
            artists_manager=ArtistsManager.create(session=session),
            current_user_manager=CurrentUserManager.create(session=session),
            playlists_manager=PlaylistsManager.create(session=session),
            users_manager=UsersManager.create(session=session),
            albums_collector=AlbumsCollector(session=session),
            tracks_collector=TracksCollector(session=session),
            audio_features_collector=AudioFeaturesCollector(session=session),
            search_collector=SearchCollector(session=session),
        )
