import pytest
from _pytest.fixtures import fixture
from aiohttp import ClientResponseError

from spotipyio import SpotifyClient
from spotipyio.consts.spotify_consts import PUBLIC, NAME, DESCRIPTION, OWNER, ID
from spotipyio.logic.creators.playlists.playlists_creation_request import PlaylistCreationRequest
from spotipyio.testing import SpotifyTestClient
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory
from spotipyio.utils import safe_nested_get
from tests.testing_utils import random_alphanumeric_string, random_boolean


class TestPlaylistsCreator:
    async def test_run__valid_request__returns_playlist(self,
                                                        test_client: SpotifyTestClient,
                                                        spotify_client: SpotifyClient,
                                                        playlist_request: PlaylistCreationRequest):
        test_client.playlists.create.expect_success(playlist_request)

        actual = await spotify_client.playlists.create.run(playlist_request)

        assert safe_nested_get(actual, [OWNER, ID]) == playlist_request.user_id
        assert actual[DESCRIPTION] == playlist_request.description
        assert actual[PUBLIC] == playlist_request.public
        assert actual[NAME] == playlist_request.name

    async def test_run__invalid_request__raises_client_response_error(self,
                                                                      test_client: SpotifyTestClient,
                                                                      spotify_client: SpotifyClient,
                                                                      playlist_request: PlaylistCreationRequest):
        test_client.playlists.create.expect_failure(playlist_request)

        with pytest.raises(ClientResponseError):
            await spotify_client.playlists.create.run(playlist_request)

    @fixture
    def playlist_request(self) -> PlaylistCreationRequest:
        return PlaylistCreationRequest(
            user_id=SpotifyMockFactory.spotify_id(),
            name=random_alphanumeric_string(),
            description=random_alphanumeric_string(),
            public=random_boolean()
        )
