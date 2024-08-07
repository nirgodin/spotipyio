from enum import Enum
from http import HTTPStatus
from random import choice, randint
from string import ascii_letters, digits
from typing import Type, List, TypeVar, Dict, Tuple, Optional

EnumType = TypeVar("EnumType", bound=Enum)
INVALID_RESPONSES = [
    (HTTPStatus.UNAUTHORIZED, "Unauthorized"),
    (HTTPStatus.FORBIDDEN, "Bad OAuth Request"),
    (HTTPStatus.TOO_MANY_REQUESTS, "Too Many Requests"),
]


def get_all_enum_values(enum_: Type[EnumType]) -> List[EnumType]:
    return [v for v in enum_]


def random_enum_value(enum_: Type[EnumType]) -> EnumType:
    enum_values = get_all_enum_values(enum_)
    return choice(enum_values)


def random_invalid_response() -> Tuple[int, Dict[str, dict]]:
    status, message = choice(INVALID_RESPONSES)
    json_response = {
        "error": {
            "status": status.value,
        }
    }

    return status.value, json_response


def random_string_dict(length: Optional[int] = None) -> Dict[str, str]:
    n_elements = length or randint(0, 10)
    return {random_alphanumeric_string(): random_alphanumeric_string() for _ in range(n_elements)}


def random_alphanumeric_string(min_length: int = 0, max_length: int = 20) -> str:
    n_chars = randint(min_length, max_length)
    characters = ascii_letters + digits

    return ''.join(choice(characters) for _ in range(n_chars))


def random_boolean() -> bool:
    return choice([True, False])
