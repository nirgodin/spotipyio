from itertools import chain
from typing import Union, List, Iterator, Optional, Any


def chain_iterable(iterable_of_iterable: Union[List[list], Iterator[list]]) -> list:
    return list(chain.from_iterable(iterable_of_iterable))


def safe_nested_get(dct: dict, paths: list, default: Optional[Any] = None) -> Any:
    value = dct.get(paths[0], {})

    for path in paths[1:]:
        value = value.get(path, {})

    return value if value else default
