from typing import List

from _pytest.fixtures import fixture

from spotipyio.logic.consts.matching_consts import FEATURE_STRINGS
from spotipyio.logic.utils import random_alphanumeric_string
from spotipyio.testing import SpotifyMockFactory
from spotipyio.tools.extractors import ArtistsEntityExtractor
from tests.testing_utils import random_string_dict


class TestArtistsEntityExtractor:
    def test_extract__no_artists__returns_empty_list(self, extractor: ArtistsEntityExtractor):
        entity = random_string_dict()
        actual = extractor.extract(entity)
        assert actual == []

    def test_extract__single_artist__returns_only_single_artist(self, extractor: ArtistsEntityExtractor):
        artist_name = random_alphanumeric_string()
        entity = self._a_track_with([artist_name])

        actual = extractor.extract(entity)

        assert actual == [artist_name]

    def test_extract__two_artists__returns_all_artists_and_all_featured_artist_combinations(
        self, extractor: ArtistsEntityExtractor
    ):
        primary_artist = random_alphanumeric_string()
        featured_artist = random_alphanumeric_string()
        artists_names = [primary_artist, featured_artist]
        featured_artists_combinations = self._build_featured_artist_combinations(primary_artist, featured_artist)
        expected = artists_names + featured_artists_combinations
        entity = self._a_track_with(artists_names)

        actual = extractor.extract(entity)

        assert actual == expected

    def test_extract__more_than_two_artists__returns_all_artists_and_single_feature_artist_combination(
        self, extractor: ArtistsEntityExtractor
    ):
        primary_artist = random_alphanumeric_string()
        first_featured_artist = random_alphanumeric_string()
        second_featured_artist = random_alphanumeric_string()
        artists_names = [primary_artist, first_featured_artist, second_featured_artist]
        featured_artist_name = f"{primary_artist}, {first_featured_artist} & {second_featured_artist}"
        expected = artists_names + [featured_artist_name]
        entity = self._a_track_with(artists_names)

        actual = extractor.extract(entity)

        assert actual == expected

    @fixture
    def extractor(self) -> ArtistsEntityExtractor:
        return ArtistsEntityExtractor()

    @staticmethod
    def _a_track_with(artists_names: List[str]) -> dict:
        artists = [SpotifyMockFactory.artist(name=name) for name in artists_names]
        return SpotifyMockFactory.track(artists=artists)

    @staticmethod
    def _build_featured_artist_combinations(primary_artist: str, featured_artist: str) -> List[str]:
        return [f"{primary_artist} {feat_string} {featured_artist}" for feat_string in FEATURE_STRINGS]
