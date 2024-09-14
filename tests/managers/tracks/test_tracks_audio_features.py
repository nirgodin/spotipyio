from typing import List, Dict

from spotipyio import SpotifyClient
from spotipyio.consts.spotify_consts import AUDIO_FEATURES
from spotipyio.consts.typing_consts import Json
from spotipyio.testing import SpotifyTestClient
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory
from tests.managers.base_chunks_collector_test import BaseChunksCollectorTest


class TestTracksAudioFeatures(BaseChunksCollectorTest):
    @property
    def _chunk_size(self) -> int:
        return 100

    @property
    def _json_response_key(self) -> str:
        return AUDIO_FEATURES

    @staticmethod
    def _a_json_response(ids: List[str]) -> Dict[str, List[Json]]:
        return SpotifyMockFactory.several_audio_features(ids)

    @staticmethod
    async def _run(ids: List[str], spotify_client: SpotifyClient) -> List[Json]:
        return await spotify_client.tracks.audio_features.run(ids)

    @staticmethod
    def _given_all_responses_unsuccessful(ids: List[str], test_client: SpotifyTestClient) -> None:
        test_client.tracks.audio_features.expect_failure(ids)

    @staticmethod
    def _given_all_responses_successful(ids: List[str], responses: List[Json], test_client: SpotifyTestClient) -> None:
        test_client.tracks.audio_features.expect_success(ids, responses)
