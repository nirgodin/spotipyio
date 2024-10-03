from random import randint

import pytest
from _pytest.fixtures import fixture
from aiohttp import ClientResponseError

from spotipyio import SpotifyClient
from spotipyio.logic.collectors.top_items_collectors.items_type import ItemsType
from spotipyio.logic.collectors.top_items_collectors.time_range import TimeRange
from spotipyio.testing import SpotifyTestClient
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory
from tests.testing_utils import random_enum_value


class TestCurrentUserTopItems:
    async def test_run__valid_response(
        self,
        test_client: SpotifyTestClient,
        spotify_client: SpotifyClient,
        items_type: ItemsType,
        time_range: TimeRange,
        limit: int,
    ):
        expected = SpotifyMockFactory.user_top_items(items_type)
        test_client.current_user.top_items.expect_success(
            items_type=items_type, time_range=time_range, limit=limit, response_json=expected
        )

        actual = await spotify_client.current_user.top_items.run(
            items_type=items_type, time_range=time_range, limit=limit
        )

        assert actual == expected

    async def test_run__invalid_response__raises_client_response_error(
        self,
        test_client: SpotifyTestClient,
        spotify_client: SpotifyClient,
        items_type: ItemsType,
        time_range: TimeRange,
        limit: int,
    ):
        test_client.current_user.top_items.expect_failure(
            items_type=items_type,
            time_range=time_range,
            limit=limit,
        )

        with pytest.raises(ClientResponseError):
            await spotify_client.current_user.top_items.run(
                items_type=items_type,
                time_range=time_range,
                limit=limit,
            )

    @fixture
    def items_type(self) -> ItemsType:
        return random_enum_value(ItemsType)

    @fixture
    def time_range(self) -> TimeRange:
        return random_enum_value(TimeRange)

    @fixture
    def limit(self) -> int:
        return randint(1, 50)
