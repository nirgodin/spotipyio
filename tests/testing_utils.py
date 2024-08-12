from enum import Enum
from random import choice
from typing import Type, List, TypeVar

EnumType = TypeVar("EnumType", bound=Enum)


def get_all_enum_values(enum_: Type[EnumType]) -> List[EnumType]:
    return [v for v in enum_]


def random_enum_value(enum_: Type[EnumType]) -> EnumType:
    enum_values = get_all_enum_values(enum_)
    return choice(enum_values)
