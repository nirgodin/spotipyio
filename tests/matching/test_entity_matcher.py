from random import random, uniform

import pytest
from _pytest.fixtures import fixture

from spotipyio.models import MatchingEntity
from spotipyio.tools.extractors import TrackEntityExtractor, PrimaryArtistEntityExtractor
from spotipyio.tools.matching import EntityMatcher
from spotipyio.testing import SpotifyMockFactory
from tests.testing_utils import random_string_dict
from spotipyio.logic.utils import random_alphanumeric_string


class TestEntityMatcher:
    def test_entity_matcher__extractors_scores_sum_not_one__raises_value_error(self):
        extractors = {TrackEntityExtractor(): random(), PrimaryArtistEntityExtractor(): random()}

        with pytest.raises(ValueError):
            EntityMatcher(extractors)

    def test_match__not_enough_fields__return_false_and_negative_score(
        self, matcher: EntityMatcher, entity: MatchingEntity
    ):
        candidate = random_string_dict()

        is_matching, score = matcher.match(entity, candidate)

        assert not is_matching
        assert score == -1

    def test_match__weighted_score_above_threshold__returns_true_and_score(
        self, matcher: EntityMatcher, entity: MatchingEntity
    ):
        candidate = SpotifyMockFactory.track(name=entity.track, artists=[SpotifyMockFactory.artist(name=entity.artist)])

        is_matching, score = matcher.match(entity, candidate)

        assert is_matching
        assert score == 1

    def test_match__weighted_score_below_threshold__returns_true_and_score(
        self, matcher: EntityMatcher, entity: MatchingEntity, threshold: float
    ):
        candidate = SpotifyMockFactory.track(
            name=random_alphanumeric_string(), artists=[SpotifyMockFactory.artist(name=random_alphanumeric_string())]
        )

        is_matching, score = matcher.match(entity, candidate)

        assert not is_matching
        assert score < threshold

    @fixture
    def matcher(self, threshold: float) -> EntityMatcher:
        track_extractor_score = random()
        extractors = {
            TrackEntityExtractor(): track_extractor_score,
            PrimaryArtistEntityExtractor(): 1 - track_extractor_score,
        }

        return EntityMatcher(extractors=extractors, threshold=threshold)

    @fixture
    def threshold(self) -> float:
        return uniform(0.7, 1)

    @fixture
    def entity(self) -> MatchingEntity:
        return MatchingEntity(
            track=random_alphanumeric_string(min_length=5), artist=random_alphanumeric_string(min_length=5)
        )
