from _pytest.fixtures import fixture

from spotipyio import TrackEntityExtractor
from spotipyio.consts.spotify_consts import NAME
from tests.testing_utils import random_alphanumeric_string, random_string_dict


class TestTrackEntityExtractor:
    def test_extract__existing_name__returns_name(self, extractor: TrackEntityExtractor):
        expected = random_alphanumeric_string()
        entity = {NAME: expected}

        actual = extractor.extract(entity)

        assert actual == expected

    def test_extract__no_name__returns_none(self, extractor: TrackEntityExtractor):
        entity = random_string_dict()
        actual = extractor.extract(entity)
        assert actual is None

    @fixture
    def extractor(self) -> TrackEntityExtractor:
        return TrackEntityExtractor()