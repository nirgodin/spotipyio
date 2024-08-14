from enum import Enum
from random import choice, randint
from string import ascii_letters, digits
from typing import Type, List, TypeVar

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
