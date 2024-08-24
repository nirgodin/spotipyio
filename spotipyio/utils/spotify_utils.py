from typing import Optional

from spotipyio.consts.spotify_consts import TRACKS, ITEMS
from spotipyio.models import EntityType
from spotipyio.utils.general_utils import safe_nested_get


def extract_first_search_result(result: dict) -> Optional[dict]:  # TODO: Add search result type parameter instead of hard-coded TRACKS
    items = safe_nested_get(result, [TRACKS, ITEMS])
    if items:
        return items[0]


def to_uri(entity_id: str, entity_type: EntityType) -> str:
    return f"spotify:{entity_type.value}:{entity_id}"
