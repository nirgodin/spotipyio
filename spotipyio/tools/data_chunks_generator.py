from math import ceil
from typing import Generator, Optional, Union

from spotipyio.consts.typing_consts import AF, F
from spotipyio.tools.pool_executor import PoolExecutor


class DataChunksGenerator:
    def __init__(self, pool_executor: PoolExecutor, chunk_size: int, max_chunks_number: Optional[int] = None):
        self._pool_executor = pool_executor
        self._chunk_size = chunk_size
        self._max_chunks_number = max_chunks_number

    async def execute_by_chunk_in_parallel(self, lst: list, filtering_list: Optional[list], func: Union[F, AF]):
        chunks = self.generate_data_chunks(lst=lst, filtering_list=filtering_list)
        return await self._pool_executor.run(
            iterable=list(chunks),
            func=func,
            expected_type=list
        )

    def generate_data_chunks(self, lst: list, filtering_list: Optional[list]) -> Generator[list, None, None]:
        if filtering_list is not None:
            lst = [elem for elem in lst if elem not in filtering_list]

        total_chunks = ceil(len(lst) / self._chunk_size)
        n_chunks = total_chunks if self._max_chunks_number is None else min(total_chunks, self._max_chunks_number)

        for i in range(0, len(lst), self._chunk_size):
            print(f'Generating chunk {self._get_chunk_number(i)} out of {n_chunks} (Total: {total_chunks})')
            yield lst[i: i + self._chunk_size]

    def _get_chunk_number(self, index: int) -> int:
        chunk_number = (index / self._chunk_size) + 1
        return int(chunk_number)
