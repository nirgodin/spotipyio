from __future__ import annotations
from spotipyio.consts.spotify_consts import SPOTIFY_API_BASE_URL
from spotipyio.logic.authentication.spotify_session import SpotifySession
from spotipyio.logic.managers import *


class SpotifyClient:
    def __init__(
        self,
        session: SpotifySession,
        albums_manager: AlbumsManager,
        artists_manager: ArtistsManager,
        chapters_manager: ChaptersManager,
        current_user_manager: CurrentUserManager,
        episodes_manager: EpisodesManager,
        playlists_manager: PlaylistsManager,
        search_manager: SearchManager,
        tracks_manager: TracksManager,
        users_manager: UsersManager,
    ):
        self.session = session
        self.albums = albums_manager
        self.artists = artists_manager
        self.chapters = chapters_manager
        self.current_user = current_user_manager
        self.episodes = episodes_manager
        self.playlists = playlists_manager
        self.search = search_manager
        self.tracks = tracks_manager
        self.users = users_manager

    @classmethod
    def create(cls, session: SpotifySession, base_url: str = SPOTIFY_API_BASE_URL) -> SpotifyClient:
        return SpotifyClient(
            session=session,
            artists_manager=ArtistsManager.create(base_url, session),
            chapters_manager=ChaptersManager.create(base_url, session),
            current_user_manager=CurrentUserManager.create(base_url, session),
            episodes_manager=EpisodesManager.create(base_url, session),
            playlists_manager=PlaylistsManager.create(base_url, session),
            users_manager=UsersManager.create(base_url, session),
            albums_manager=AlbumsManager.create(base_url, session),
            tracks_manager=TracksManager.create(base_url, session),
            search_manager=SearchManager.create(base_url, session),
        )
