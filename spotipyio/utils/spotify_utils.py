from base64 import b64encode
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


def encode_bearer_token(client_id: str, client_secret: str) -> str:
    bytes_auth = bytes(f"{client_id}:{client_secret}", "ISO-8859-1")
    b64_auth = b64encode(bytes_auth)

    return b64_auth.decode('ascii')
