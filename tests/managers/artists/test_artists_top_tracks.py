from spotipyio import SpotifyClient
from spotipyio.testing import SpotifyTestClient
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory


class TestArtistsTopTracks:
    async def test_run_single__single_chunk__valid_response(self,
                                                            test_client: SpotifyTestClient,
                                                            spotify_client: SpotifyClient):
        artist_id = SpotifyMockFactory.spotify_id()
        expected = SpotifyMockFactory.several_tracks()
        request_handlers = test_client.artists.top_tracks.expect([artist_id])
        request_handlers[0].respond_with_json(expected)

        actual = await spotify_client.artists.top_tracks.run_single(artist_id)

        assert actual == expected
