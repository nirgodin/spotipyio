from typing import Dict, List

import pytest
from _pytest.fixtures import fixture

from spotipyio.logic.consts.spotify_consts import ARTISTS
from spotipyio.logic.entity_extractors import PrimaryArtistEntityExtractor
from spotipyio.testing.spotify_mock_factory import SpotifyMockFactory
from tests.testing_utils import random_string_dict, random_alphanumeric_string


class TestPrimaryArtistEntityExtractor:
    def test_extract__with_artists__returns_first_artist_name(
        self, extractor: PrimaryArtistEntityExtractor, primary_artist_name: str, entity: Dict[str, List[Dict[str, str]]]
    ):
        actual = extractor.extract(entity)
        assert actual == primary_artist_name

    @pytest.mark.parametrize("entity", [random_string_dict(), {ARTISTS: []}, {ARTISTS: [random_string_dict()]}])
    def test_extract__no_artists__returns_none(self, entity: dict, extractor: PrimaryArtistEntityExtractor):
        actual = extractor.extract(entity)
        assert actual is None

    @fixture
    def extractor(self) -> PrimaryArtistEntityExtractor:
        return PrimaryArtistEntityExtractor()

    @fixture
    def primary_artist_name(self) -> str:
        return random_alphanumeric_string()

    @fixture
    def entity(self, primary_artist_name: str) -> Dict[str, List[Dict[str, str]]]:
        primary_artist = SpotifyMockFactory.artist(name=primary_artist_name)
        artists = SpotifyMockFactory.several_artists()
        artists[ARTISTS].insert(0, primary_artist)

        return artists
