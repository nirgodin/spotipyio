from random import choice, randint
from typing import List

from _pytest.fixtures import fixture

from spotipyio.logic.consts.matching_consts import LOWERCASED_FEATURE_STRINGS
from spotipyio.logic.consts.spotify_consts import NAME
from spotipyio.logic.utils import random_alphanumeric_string
from spotipyio.testing import SpotifyMockFactory
from spotipyio.tools.extractors import TrackEntityExtractor
from tests.testing_utils import random_string_dict, random_string_array


class TestTrackEntityExtractor:
    def test_extract__existing_name__returns_name(self, extractor: TrackEntityExtractor):
        expected = random_alphanumeric_string()
        entity = {NAME: expected}

        actual = extractor.extract(entity)

        assert actual == [expected]

    def test_extract__no_name__returns_empty_list(self, extractor: TrackEntityExtractor):
        entity = random_string_dict()
        actual = extractor.extract(entity)
        assert actual == []

    def test_extract__with_featured_artists__returns_original_name_and_name_without_artists(
        self, extractor: TrackEntityExtractor
    ):
        artists_names = random_string_array(length=randint(1, 10))
        artists = [SpotifyMockFactory.artist(name=artist_name) for artist_name in artists_names]
        track_name = random_alphanumeric_string()
        track_name_with_featured_artist = self._build_track_name_with_featured_strings(track_name, artists_names)
        entity = SpotifyMockFactory.track(name=track_name_with_featured_artist, artists=artists)

        actual = extractor.extract(entity)

        assert actual == [track_name_with_featured_artist, track_name.lower()]

    @fixture
    def extractor(self) -> TrackEntityExtractor:
        return TrackEntityExtractor()

    @staticmethod
    def _build_track_name_with_featured_strings(raw_track_name: str, artists_names: List[str]) -> str:
        name_components = [raw_track_name]

        for artist_name in artists_names:
            feature_string = choice(LOWERCASED_FEATURE_STRINGS)
            name_components.extend([feature_string, artist_name])

        return " ".join(name_components)
