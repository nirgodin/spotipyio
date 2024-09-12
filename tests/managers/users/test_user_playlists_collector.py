import pytest
from _pytest.fixtures import fixture
from aiohttp import ClientResponseError

from spotipyio import SpotifyClient
from spotipyio.testing import SpotifyTestClient
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory


class TestUserPlaylistsCollector:
    async def test_run_single__valid_request__returns_paged_playlists(self,
                                                                      spotify_client: SpotifyClient,
                                                                      test_client: SpotifyTestClient,
                                                                      user_id: str,
                                                                      paged_playlist: dict):
        test_client.users.playlists.expect_success(user_id, response_json=paged_playlist)
        actual = await spotify_client.users.playlists.run_single(user_id)
        assert actual == paged_playlist

    async def test_run_single__invalid_request__raises_client_response_error(self,
                                                                             spotify_client: SpotifyClient,
                                                                             test_client: SpotifyTestClient,
                                                                             user_id: str):
        test_client.users.playlists.expect_failure(user_id)

        with pytest.raises(ClientResponseError):
            await spotify_client.users.playlists.run_single(user_id)

    @fixture
    def user_id(self) -> str:
        return SpotifyMockFactory.spotify_id()

    @fixture
    def paged_playlist(self, user_id: str) -> dict:
        return SpotifyMockFactory.paged_playlists(id=user_id)
