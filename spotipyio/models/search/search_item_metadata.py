from dataclasses import dataclass, field
from typing import List

from spotipyio.models.search.spotify_search_type import SpotifySearchType


@dataclass
class SearchItemMetadata:
    search_types: List[SpotifySearchType] = field(default_factory=lambda: [v for v in SpotifySearchType])
    quote: bool = True

    def __post_init__(self):
        if not self.search_types:
            raise ValueError("SearchItemMetadata must include at least one SpotifySearchType")
