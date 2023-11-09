from dataclasses import dataclass, fields
from typing import Optional, List, Dict
from urllib.parse import quote

from spotipyio.logic.collectors.search_collectors.spotify_search_type import SpotifySearchType

SEARCH_TYPES = "search_types"


@dataclass
class SearchItem:
    search_types: List[SpotifySearchType]
    track: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    year: Optional[int] = None
    # TODO: Add missing fields options

    def __post_init__(self):
        self._validate_input()

    def to_query_params(self) -> Dict[str, str]:
        types = [search_type.value for search_type in self.search_types]
        query = self._build_query()
        return {
            "q": query,
            "types": ",".join(types)
        }

    def _build_query(self) -> str:
        query_components = []

        for field in fields(self):
            if field.name != SEARCH_TYPES:
                field_value = getattr(self, field.name)

                if field_value is not None:
                    query_components.append(f"{field.name}:{field_value}")

        return quote(" ".join(query_components))

    def _validate_input(self) -> None:
        fields_values = [getattr(self, field.name) for field in fields(self) if field.name != SEARCH_TYPES]

        if all(value is None for value in fields_values):
            raise ValueError("You must supply at least one search value")
