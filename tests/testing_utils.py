import os
from enum import Enum
from random import choice, randint
from string import ascii_letters, digits
from typing import Type, List, TypeVar, Any, Callable, Optional, Dict

EnumType = TypeVar("EnumType", bound=Enum)


def get_all_enum_values(enum_: Type[EnumType]) -> List[EnumType]:
    return [v for v in enum_]


def random_enum_value(enum_: Type[EnumType]) -> EnumType:
    enum_values = get_all_enum_values(enum_)
    return choice(enum_values)


def random_boolean() -> bool:
    return choice([True, False])


def random_alphanumeric_string(min_length: int = 1, max_length: int = 20) -> str:
    n_chars = randint(min_length, max_length)
    characters = ascii_letters + digits

    return ''.join(choice(characters) for _ in range(n_chars))


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
