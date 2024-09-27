from random import randint, shuffle
from typing import List, Tuple

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
                                                                         test_client: SpotifyTestClient):
        search_item = SpotifyMockFactory.search_item()
        expected = SpotifyMockFactory.search_response(search_item)
        test_client.search.search_item.expect_success(search_item, expected)

        actual = await spotify_client.search.search_item.run_single(search_item)

        assert actual == expected

    async def test_run_single__invalid_response__raises_client_response_error(self,
                                                                              spotify_client: SpotifyClient,
                                                                              test_client: SpotifyTestClient):
        search_item = SpotifyMockFactory.search_item()
        test_client.search.search_item.expect_failure(search_item)

        with pytest.raises(ClientResponseError):
            await spotify_client.search.search_item.run_single(search_item)

    async def test_run__valid_response(self,
                                       valid_search_items: List[SearchItem],
                                       search_items_responses_map: List[Tuple[SearchItem, dict]],
                                       test_client: SpotifyTestClient,
                                       spotify_client: SpotifyClient):
        self._given_all_responses_valid(search_items_responses_map, test_client)
        expected = [response for _, response in search_items_responses_map]

        actual = await spotify_client.search.search_item.run(valid_search_items)

        assert actual == expected

    async def test_run__all_invalid_responses__returns_empty_list(self,
                                                                  invalid_search_items: List[SearchItem],
                                                                  test_client: SpotifyTestClient,
                                                                  spotify_client: SpotifyClient):
        self._given_all_responses_invalid(invalid_search_items, test_client)
        actual = await spotify_client.search.search_item.run(invalid_search_items)
        assert actual == []

    async def test_run__mixed_responses__returns_only_valid(self,
                                                            valid_search_items: List[SearchItem],
                                                            invalid_search_items: List[SearchItem],
                                                            search_items_responses_map: List[Tuple[SearchItem, dict]],
                                                            test_client: SpotifyTestClient,
                                                            spotify_client: SpotifyClient):
        self._given_all_responses_valid(search_items_responses_map, test_client)
        self._given_all_responses_invalid(invalid_search_items, test_client)
        expected = [response for _, response in search_items_responses_map]
        search_items = valid_search_items + invalid_search_items
        shuffle(search_items)

        actual = await spotify_client.search.search_item.run(search_items)

        assert all(response in expected for response in actual)
        assert all(response in actual for response in expected)

    @fixture
    def invalid_search_items(self) -> List[SearchItem]:
        items_number = randint(1, 10)
        return [SpotifyMockFactory.search_item() for _ in range(items_number)]

    @fixture
    def valid_search_items(self) -> List[SearchItem]:
        items_number = randint(1, 10)
        return [SpotifyMockFactory.search_item() for _ in range(items_number)]

    @fixture
    def search_items_responses_map(self, valid_search_items: List[SearchItem]) -> List[Tuple[SearchItem, dict]]:
        search_items_map = []

        for search_item in valid_search_items:
            response = SpotifyMockFactory.search_response(search_item)
            search_items_map.append((search_item, response))

        return search_items_map

    @staticmethod
    def _given_all_responses_valid(search_items_responses_map: List[Tuple[SearchItem, dict]],
                                   test_client: SpotifyTestClient) -> None:
        for search_item, response_json in search_items_responses_map:
            test_client.search.search_item.expect_success(search_item=search_item, response_json=response_json)

    @staticmethod
    def _given_all_responses_invalid(search_items: List[SearchItem], test_client: SpotifyTestClient) -> None:
        for search_item in search_items:
            test_client.search.search_item.expect_failure(search_item)
