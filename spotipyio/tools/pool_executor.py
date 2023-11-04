from functools import partial
from typing import Iterable, Any, List, Sized

from asyncio_pool import AioPool
from tqdm import tqdm

from spotipyio.consts.general_consts import AIO_POOL_SIZE
from spotipyio.consts.typing_consts import AF
from spotipyio.tools.logging import logger


class PoolExecutor:
    @staticmethod
    async def run(iterable: Sized, func: AF) -> List[Any]:
        pool = AioPool(AIO_POOL_SIZE)

        with tqdm(total=len(iterable)) as progress_bar:
            monitored_func = partial(PoolExecutor._execute_single, progress_bar, func)
            return await pool.map(monitored_func, iterable)

    @staticmethod
    async def _execute_single(progress_bar: tqdm, func: AF, value: Any) -> Any:
        try:
            return await func(value)

        except Exception as e:
            logger.exception("PoolExecutor encountered exception")
            return e

        finally:
            progress_bar.update(1)
