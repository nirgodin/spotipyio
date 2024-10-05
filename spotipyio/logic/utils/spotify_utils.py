from base64 import b64encode

from spotipyio.models import EntityType


def to_uri(entity_id: str, entity_type: EntityType) -> str:
    return f"spotify:{entity_type.value}:{entity_id}"


def encode_bearer_token(client_id: str, client_secret: str) -> str:
    bytes_auth = bytes(f"{client_id}:{client_secret}", "ISO-8859-1")
    b64_auth = b64encode(bytes_auth)

    return b64_auth.decode("ascii")
