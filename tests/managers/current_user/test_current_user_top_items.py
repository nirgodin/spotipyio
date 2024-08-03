import pytest
from _pytest.fixtures import fixture
from aiohttp import ClientResponseError

from spotipyio import SpotifyClient
from spotipyio.logic.collectors.top_items_collectors.items_type import ItemsType
from spotipyio.logic.collectors.top_items_collectors.time_range import TimeRange
from spotipyio.testing import SpotifyTestClient
from tests.testing_utils import random_enum_value, random_invalid_response, random_string_dict


class TestCurrentUserTopItems:
    async def test_run__valid_response(self,
                                       test_client: SpotifyTestClient,
                                       spotify_client: SpotifyClient,
                                       items_type: ItemsType,
                                       time_range: TimeRange):
        expected = random_string_dict()
        test_client.current_user.top_items \
            .expect(items_type=items_type, time_range=time_range) \
            .respond_with_json(expected)

        actual = await spotify_client.current_user.top_items.run(
            items_type=items_type,
            time_range=time_range
        )

        assert actual == expected

    async def test_run__invalid_response__raises_client_response_error(self,
                                                                       test_client: SpotifyTestClient,
                                                                       spotify_client: SpotifyClient,
                                                                       items_type: ItemsType,
                                                                       time_range: TimeRange):
        expected_status_code, expected_response = random_invalid_response()
        test_client.current_user.top_items \
            .expect(items_type=items_type, time_range=time_range) \
            .respond_with_json(expected_response, status=expected_status_code)

        with pytest.raises(ClientResponseError) as exc_info:
            await spotify_client.current_user.top_items.run(
                items_type=items_type,
                time_range=time_range
            )

        assert exc_info.value.code == expected_status_code
        assert exc_info.value.message.endswith(str(expected_response))

    @fixture
    def items_type(self) -> ItemsType:
        return random_enum_value(ItemsType)

    @fixture
    def time_range(self) -> ItemsType:
        return random_enum_value(ItemsType)
