from __future__ import annotations
from spotipyio.consts.spotify_consts import SPOTIFY_API_BASE_URL
from spotipyio.logic.authentication.spotify_session import SpotifySession
from spotipyio.logic.managers import (
    AlbumsManager,
    ArtistsManager,
    ChaptersManager,
    CurrentUserManager,
    EpisodesManager,
    PlaylistsManager,
    SearchManager,
    TracksManager,
    UsersManager,
)


class SpotifyClient:
    def __init__(
        self,
        session: SpotifySession,
        albums: AlbumsManager,
        artists: ArtistsManager,
        chapters: ChaptersManager,
        current_user: CurrentUserManager,
        episodes: EpisodesManager,
        playlists: PlaylistsManager,
        search: SearchManager,
        tracks: TracksManager,
        users: UsersManager,
    ):
        self.session = session
        self.albums = albums
        self.artists = artists
        self.chapters = chapters
        self.current_user = current_user
        self.episodes = episodes
        self.playlists = playlists
        self.search = search
        self.tracks = tracks
        self.users = users

    @classmethod
    def create(cls, session: SpotifySession, base_url: str = SPOTIFY_API_BASE_URL) -> SpotifyClient:
        return SpotifyClient(
            session=session,
            artists=ArtistsManager.create(base_url, session),
            chapters=ChaptersManager.create(base_url, session),
            current_user=CurrentUserManager.create(base_url, session),
            episodes=EpisodesManager.create(base_url, session),
            playlists=PlaylistsManager.create(base_url, session),
            users=UsersManager.create(base_url, session),
            albums=AlbumsManager.create(base_url, session),
            tracks=TracksManager.create(base_url, session),
            search=SearchManager.create(base_url, session),
        )
