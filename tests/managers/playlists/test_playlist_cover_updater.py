import pytest
from _pytest.fixtures import fixture
from aiohttp import ClientResponseError

from spotipyio import SpotifyClient
from spotipyio.testing import SpotifyTestClient
from tests.testing_utils import random_bytes


class TestPlaylistCoverUpdater:
    async def test_run__valid_request__returns_none(self,
                                                    spotify_client: SpotifyClient,
                                                    test_client: SpotifyTestClient,
                                                    playlist_id: str,
                                                    image: bytes):
        test_client.playlists.update_cover.expect_success(
            playlist_id=playlist_id,
            image=image
        )
        actual = await spotify_client.playlists.update_cover.run(
            playlist_id=playlist_id,
            image=image,
            compress_if_needed=False
        )
        assert actual is None

    async def test_run__invalid_request__raises_client_response_error(self,
                                                                      spotify_client: SpotifyClient,
                                                                      test_client: SpotifyTestClient,
                                                                      playlist_id: str,
                                                                      image: bytes):
        test_client.playlists.update_cover.expect_failure(
            playlist_id=playlist_id,
            image=image
        )

        with pytest.raises(ClientResponseError):
            await spotify_client.playlists.update_cover.run(
                playlist_id=playlist_id,
                image=image,
                compress_if_needed=False
            )

    @fixture
    def image(self) -> bytes:
        return random_bytes()
