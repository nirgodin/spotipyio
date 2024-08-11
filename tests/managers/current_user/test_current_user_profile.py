import pytest
from aiohttp import ClientResponseError

from spotipyio import SpotifyClient
from spotipyio.testing import SpotifyTestClient
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory


class TestCurrentUserProfile:
    async def test_run__valid_response(self, test_client: SpotifyTestClient, spotify_client: SpotifyClient):
        expected = SpotifyMockFactory.user_profile()
        test_client.current_user.profile.expect_success(expected)

        actual = await spotify_client.current_user.profile.run()

        assert actual == expected

    async def test_run__invalid_response__raises_client_response_error(self,
                                                                       test_client: SpotifyTestClient,
                                                                       spotify_client: SpotifyClient):
        test_client.current_user.profile.expect_failure()

        with pytest.raises(ClientResponseError):
            await spotify_client.current_user.profile.run()
