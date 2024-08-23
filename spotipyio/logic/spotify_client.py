from __future__ import annotations
from spotipyio.consts.spotify_consts import SPOTIFY_API_BASE_URL
from spotipyio.logic.authentication.spotify_session import SpotifySession
from spotipyio.logic.managers import *


class SpotifyClient:
    def __init__(self,
                 session: SpotifySession,
                 artists_manager: ArtistsManager,
                 current_user_manager: CurrentUserManager,
                 playlists_manager: PlaylistsManager,
                 users_manager: UsersManager,
                 albums_manager: AlbumsManager,
                 tracks_manager: TracksManager,
                 search_manager: SearchManager):
        self.session = session
        self.artists = artists_manager
        self.albums = albums_manager
        self.tracks = tracks_manager
        self.users = users_manager
        self.playlists = playlists_manager
        self.search = search_manager
        self.current_user = current_user_manager

    @classmethod
    def create(cls, session: SpotifySession, base_url: str = SPOTIFY_API_BASE_URL) -> SpotifyClient:
        return SpotifyClient(
            session=session,
            artists_manager=ArtistsManager.create(session=session, base_url=base_url),
            current_user_manager=CurrentUserManager.create(session=session, base_url=base_url),
            playlists_manager=PlaylistsManager.create(session=session, base_url=base_url),
            users_manager=UsersManager.create(session=session, base_url=base_url),
            albums_manager=AlbumsManager.create(session=session, base_url=base_url),
            tracks_manager=TracksManager.create(session=session, base_url=base_url),
            search_manager=SearchManager.create(session=session, base_url=base_url),
        )
