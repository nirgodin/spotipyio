from dataclasses import dataclass, field
from typing import List

from spotipyio.logic.collectors.search_collectors.spotify_search_type import SpotifySearchType


@dataclass
class SearchItemMetadata:
    search_types: List[SpotifySearchType] = field(default_factory=lambda: [v for v in SpotifySearchType])
    quote: bool = True
