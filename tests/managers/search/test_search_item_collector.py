import pytest
from aiohttp import ClientResponseError
from pytest_asyncio import fixture

from spotipyio import SpotifyClient
from spotipyio.models import SearchItem
from spotipyio.testing import SpotifyTestClient
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory


class TestSearchItemCollector:
    async def test_run_single__valid_response__returns_expected_response(self,
                                                                         spotify_client: SpotifyClient,
                                                                         test_client: SpotifyTestClient,
                                                                         search_item: SearchItem):
        expected = SpotifyMockFactory.search_response(search_item.metadata.search_types)
        test_client.search.search_item.expect_success(search_item, expected)

        actual = await spotify_client.search.search_item.run_single(search_item)

        assert actual == expected

    async def test_run_single__invalid_response__raises_client_response_error(self,
                                                                              spotify_client: SpotifyClient,
                                                                              test_client: SpotifyTestClient,
                                                                              search_item: SearchItem):
        test_client.search.search_item.expect_failure(search_item)

        with pytest.raises(ClientResponseError):
            await spotify_client.search.search_item.run_single(search_item)

    @fixture
    def search_item(self) -> SearchItem:
        return SpotifyMockFactory.search_item()
