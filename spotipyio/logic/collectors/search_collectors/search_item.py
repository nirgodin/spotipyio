from dataclasses import dataclass, fields
from typing import Optional, Dict, List
from urllib.parse import quote

from spotipyio.logic.collectors.search_collectors.search_item_filters import SearchItemFilters
from spotipyio.logic.collectors.search_collectors.search_item_metadata import SearchItemMetadata


@dataclass
class SearchItem:
    text: Optional[str] = None
    filters: SearchItemFilters = SearchItemFilters()
    metadata: SearchItemMetadata = SearchItemMetadata()

    def __post_init__(self):
        self._validate_input()

    def to_query_params(self) -> Dict[str, str]:
        types = [search_type.value for search_type in self.metadata.search_types]
        query = self._build_query()

        return {
            "q": query,
            "type": ",".join(types)
        }

    def _build_query(self) -> str:
        query_components = self._get_query_component()
        query = " ".join(query_components)

        if self.metadata.quote:
            return quote(query)

        return query

    def _get_query_component(self) -> List[str]:
        query_components = []

        if self.text is not None:
            query_components.append(self.text)

        for field in fields(self.filters):
            field_value = getattr(self.filters, field.name)

            if field_value is not None:
                query_components.append(f"{field.name}:{field_value}")

        return query_components

    def _validate_input(self) -> None:
        filters_values = [getattr(self.filters, field.name) for field in fields(self.filters)]
        are_all_filters_missing = all(value is None for value in filters_values)

        if self.text is None and are_all_filters_missing:
            raise ValueError("You must supply text or at least one search filter")
