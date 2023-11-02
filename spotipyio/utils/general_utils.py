from itertools import chain
from typing import Union, List, Iterator


def chain_iterable(iterable_of_iterable: Union[List[list], Iterator[list]]) -> list:
    return list(chain.from_iterable(iterable_of_iterable))
