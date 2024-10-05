import os
from random import choice, randint
from typing import Type, List, Any, Callable, Optional, Dict
from urllib.parse import urlencode

from spotipyio.logic.consts.typing_consts import EnumType
from spotipyio.logic.utils import random_alphanumeric_string


def get_all_enum_values(enum_: Type[EnumType]) -> List[EnumType]:
    return [v for v in enum_]


def random_enum_value(enum_: Type[EnumType]) -> EnumType:
    enum_values = get_all_enum_values(enum_)
    return choice(enum_values)


def random_multi_enum_values(enum_: Type[EnumType]) -> List[EnumType]:
    enum_values = get_all_enum_values(enum_)
    return [v for v in enum_values if random_boolean()]


def random_boolean() -> bool:
    return choice([True, False])


def an_optional(value_generator: Callable[[], Any]) -> Optional[Any]:
    if random_boolean():
        return value_generator()


def random_bytes(size: Optional[int] = None) -> bytes:
    n_bytes = size or randint(1, 100)
    return os.urandom(n_bytes)


def random_string_dict(length: Optional[int] = None) -> Dict[str, str]:
    n_elements = length or randint(0, 10)
    return {random_alphanumeric_string(): random_alphanumeric_string() for _ in range(n_elements)}


def assert_sorted_equal(actual: List[dict], expected: List[dict], sort_by: str) -> None:
    assert sorted(actual, key=lambda x: x[sort_by]) == sorted(expected, key=lambda x: x[sort_by])


def build_request_data(data: dict) -> bytes:
    return bytes(urlencode(data).encode())


def random_string_array(length: Optional[int] = None) -> List[str]:
    n_elements = length or randint(0, 10)
    return [random_alphanumeric_string() for _ in range(n_elements)]


def random_port() -> int:
    return randint(1000, 10000)


def random_localhost_url() -> str:
    return f"http://localhost:{random_port()}"
