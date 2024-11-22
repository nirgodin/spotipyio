from typing import List

import pytest
from aiohttp import ClientResponseError

from spotipyio import SpotifyClient
from spotipyio.testing import SpotifyTestClient, SpotifyMockFactory


class TestPlaylistsItemsReplacer:
    async def test_run__valid_request__returns_snapshot_id(
        self,
        test_client: SpotifyTestClient,
        spotify_client: SpotifyClient,
        playlist_id: str,
        uris: List[str],
    ):
        expected = SpotifyMockFactory.snapshot_response()
        test_client.playlists.replace_items.expect_success(playlist_id=playlist_id, uris=uris, response_json=expected)

        actual = await spotify_client.playlists.replace_items.run(playlist_id, uris)

        assert actual == expected

    async def test_run__invalid_request__raises_client_response_error(
        self, test_client: SpotifyTestClient, spotify_client: SpotifyClient, playlist_id: str, uris: List[str]
    ):
        test_client.playlists.replace_items.expect_failure(playlist_id, uris)

        with pytest.raises(ClientResponseError):
            await spotify_client.playlists.replace_items.run(playlist_id, uris)
