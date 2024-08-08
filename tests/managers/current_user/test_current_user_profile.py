import pytest
from aiohttp import ClientResponseError

from spotipyio import SpotifyClient
from spotipyio.testing import SpotifyTestClient
from tests.testing_utils import random_invalid_response, random_string_dict


class TestCurrentUserProfile:
    async def test_run__valid_response(self, test_client: SpotifyTestClient, spotify_client: SpotifyClient):
        expected = random_string_dict()
        request_handlers = test_client.current_user.profile.expect()
        request_handlers[0].respond_with_json(expected)

        actual = await spotify_client.current_user.profile.run()

        assert actual == expected

    async def test_run__invalid_response__raises_client_response_error(self,
                                                                       test_client: SpotifyTestClient,
                                                                       spotify_client: SpotifyClient):
        expected_status_code, expected_response = random_invalid_response()
        request_handlers = test_client.current_user.profile.expect()
        request_handlers[0].respond_with_json(response_json=expected_response, status=expected_status_code)

        with pytest.raises(ClientResponseError) as exc_info:
            await spotify_client.current_user.profile.run()

        assert exc_info.value.code == expected_status_code
        assert exc_info.value.message.endswith(str(expected_response))
