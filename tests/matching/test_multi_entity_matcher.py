from random import randint, random, choice
from typing import List, Tuple
from unittest.mock import MagicMock

import pytest
from _pytest.fixtures import fixture

from spotipyio.logic.utils import get_all_enum_values
from spotipyio.models import MatchingEntity, MatchingMethod
from spotipyio.testing import SpotifyMockFactory
from spotipyio.tools.matching import EntityMatcher, MultiEntityMatcher


class TestMultiEntityMatcher:
    @pytest.mark.parametrize("matching_method", get_all_enum_values(MatchingMethod))
    def test_match__no_matching_candidate__returns_none(
        self,
        matching_method: MatchingMethod,
        mock_entity_matcher: MagicMock,
        multi_entity_matcher: MultiEntityMatcher,
        entities: List[MatchingEntity],
        candidates: List[dict],
    ):
        self._given_no_candidate_is_matching(mock_entity_matcher)
        actual = multi_entity_matcher.match(entities=entities, candidates=candidates, method=matching_method)
        assert actual is None

    def test_match__first_matching_method__returns_first_matching_even_if_latest_has_higher_score(
        self,
        mock_entity_matcher: MagicMock,
        multi_entity_matcher: MultiEntityMatcher,
        entities: List[MatchingEntity],
        candidates: List[dict],
        first_matching_candidate: dict,
        second_matching_candidate: dict,
    ):
        self._given_two_matching_candidates_first_with_lower_score(
            mock_entity_matcher=mock_entity_matcher,
            first_matching_candidate=first_matching_candidate,
            second_matching_candidate=second_matching_candidate,
        )

        actual = multi_entity_matcher.match(
            entities=entities, candidates=candidates, method=MatchingMethod.FIRST_MATCHING
        )

        assert actual == first_matching_candidate

    def test_match__highest_match_score_method__returns_highest_score_candidate(
        self,
        mock_entity_matcher: MagicMock,
        multi_entity_matcher: MultiEntityMatcher,
        entities: List[MatchingEntity],
        candidates: List[dict],
        first_matching_candidate: dict,
        second_matching_candidate: dict,
    ):
        self._given_two_matching_candidates_first_with_lower_score(
            mock_entity_matcher=mock_entity_matcher,
            first_matching_candidate=first_matching_candidate,
            second_matching_candidate=second_matching_candidate,
        )

        actual = multi_entity_matcher.match(
            entities=entities, candidates=candidates, method=MatchingMethod.HIGHEST_MATCH_SCORE
        )

        assert actual == second_matching_candidate

    @fixture
    def multi_entity_matcher(self, mock_entity_matcher: MagicMock) -> MultiEntityMatcher:
        return MultiEntityMatcher(mock_entity_matcher)

    @fixture
    def mock_entity_matcher(self) -> MagicMock(EntityMatcher):
        return MagicMock(EntityMatcher)

    @fixture
    def entities(self) -> List[MatchingEntity]:
        entities_number = randint(1, 10)
        return [SpotifyMockFactory.matching_entity() for _ in range(entities_number)]

    @fixture
    def candidates(self) -> List[dict]:
        candidates_number = randint(2, 10)
        return [SpotifyMockFactory.track() for _ in range(candidates_number)]

    @fixture
    def first_matching_candidate_index(self, candidates: List[dict]) -> int:
        return choice(range(len(candidates) - 1))

    @fixture
    def first_matching_candidate(self, candidates: List[dict], first_matching_candidate_index: int) -> dict:
        return candidates[first_matching_candidate_index]

    @fixture
    def second_matching_candidate(self, candidates: List[dict], first_matching_candidate_index: int) -> dict:
        return candidates[first_matching_candidate_index + 1]

    @staticmethod
    def _given_no_candidate_is_matching(mock_entity_matcher: MagicMock) -> None:
        mock_entity_matcher.match.side_effect = lambda entity, candidate: (False, random())

    @staticmethod
    def _given_two_matching_candidates_first_with_lower_score(
        mock_entity_matcher: MagicMock, first_matching_candidate: dict, second_matching_candidate: dict
    ) -> None:
        highest_match_score = random()

        def _mock_match(entity: MatchingEntity, candidate: dict) -> Tuple[bool, float]:
            if candidate == first_matching_candidate:
                return True, highest_match_score - 0.01

            if candidate == second_matching_candidate:
                return True, highest_match_score

            return False, highest_match_score - random()

        mock_entity_matcher.match.side_effect = _mock_match
