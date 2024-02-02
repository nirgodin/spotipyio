from dataclasses import fields, Field
from typing import Tuple, List, Optional, Dict, Any

from spotipyio.logic.entity_extractors import TrackEntityExtractor, ArtistEntityExtractor
from spotipyio.contract import IEntityExtractor
from spotipyio.logic.entity_matching.matching_entity import MatchingEntity
from spotipyio.utils import compute_similarity_score


class EntityMatcher:
    def __init__(self,
                 extractors: Optional[Dict[IEntityExtractor, float]] = None,
                 threshold: float = 0.7,
                 min_present_fields: int = 2):
        self._extractors = extractors or self._get_default_extractors()
        self._threshold = threshold
        self._min_present_fields = min_present_fields

    def match(self, entity: MatchingEntity, candidate: Any) -> Tuple[bool, float]:
        scores = []

        for field in fields(entity):
            field_score = self._compute_field_score(entity, field, candidate)

            if field_score is not None:
                scores.append(field_score)

        return self._is_matching(scores)

    def _compute_field_score(self, entity, field: Field, raw_candidate: Any) -> Optional[float]:
        extractor = self._names_to_extractors[field.name]
        extractor_score = self._names_to_scores[field.name]
        entity = getattr(entity, field.name)

        if entity is not None:
            score = self._compute_raw_field_score(extractor, raw_candidate, entity)

            if score is not None:
                return score * extractor_score

    @staticmethod
    def _compute_raw_field_score(extractor: IEntityExtractor, raw_candidate: Any, entity: str) -> Optional[float]:
        candidate = extractor.extract(raw_candidate)

        if candidate is not None:
            return compute_similarity_score(candidate, entity)

    @staticmethod
    def _get_default_extractors() -> Dict[IEntityExtractor, float]:
        return {
            TrackEntityExtractor(): 0.7,
            ArtistEntityExtractor(): 0.3
        }

    @property
    def _names_to_extractors(self) -> Dict[str, IEntityExtractor]:
        return {extractor.name: extractor for extractor in self._extractors.keys()}

    @property
    def _names_to_scores(self) -> Dict[str, float]:
        return {extractor.name: score for extractor, score in self._extractors.items()}

    def _is_matching(self, scores: List[float]) -> Tuple[bool, float]:
        if len(scores) < self._min_present_fields:
            return False, -1

        weighted_score = sum(scores)
        is_matching = weighted_score >= self._threshold

        return is_matching, weighted_score
