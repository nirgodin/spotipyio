from pytest_asyncio import fixture

from spotipyio import SpotifyClient
from spotipyio.models import SearchItem
from spotipyio.testing import SpotifyTestClient


class TestSearchItemCollector:
    async def test_run_single__invalid_response__raises_client_response_error(self,
                                                                              spotify_client: SpotifyClient,
                                                                              test_client: SpotifyTestClient):
        test_client.search.search_item.expect_failure()

    @fixture
    def search_item(self) -> SearchItem:
        return SearchItem()
