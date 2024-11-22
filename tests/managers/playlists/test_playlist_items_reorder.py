from random import randint

import pytest
from _pytest.fixtures import fixture
from aiohttp import ClientResponseError

from spotipyio import SpotifyClient
from spotipyio.models.playlist_reorder_request import PlaylistReorderRequest
from spotipyio.testing import SpotifyTestClient, SpotifyMockFactory


class TestPlaylistsItemsReorder:
    async def test_run__valid_request__returns_snapshot_id(
        self,
        test_client: SpotifyTestClient,
        spotify_client: SpotifyClient,
        reorder_request: PlaylistReorderRequest,
    ):
        expected = SpotifyMockFactory.snapshot_response()
        test_client.playlists.reorder_items.expect_success(request=reorder_request, response_json=expected)

        actual = await spotify_client.playlists.reorder_items.run(reorder_request)

        assert actual == expected

    async def test_run__invalid_request__raises_client_response_error(
        self,
        test_client: SpotifyTestClient,
        spotify_client: SpotifyClient,
        reorder_request: PlaylistReorderRequest,
    ):
        test_client.playlists.reorder_items.expect_failure(reorder_request)

        with pytest.raises(ClientResponseError):
            await spotify_client.playlists.reorder_items.run(reorder_request)

    @fixture
    def reorder_request(self, playlist_id: str) -> PlaylistReorderRequest:
        return PlaylistReorderRequest(
            playlist_id="",
            range_start=randint(1, 100),
            insert_before=randint(1, 100),
            snapshot_id=SpotifyMockFactory.snapshot_id(),
            range_length=randint(1, 100),
        )
