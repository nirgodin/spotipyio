import json
from typing import Dict

from _pytest.fixtures import fixture
from redis import Redis

from spotipyio.extras.redis import RedisSessionCacheHandler
from tests.extras.redis.redis_testkit import RedisTestkit
from tests.testing_utils import random_alphanumeric_string, random_string_dict


class TestRedisSessionCacheHandler:
    @fixture(autouse=True)
    def teardown(self, redis: Redis, response: Dict[str, str]) -> None:
        yield
        redis.flushdb()

    def test_get__existing_key__returns_stored_value(self,
                                                     cache_handler: RedisSessionCacheHandler,
                                                     redis: Redis,
                                                     cache_key: str,
                                                     response: Dict[str, str]):
        redis.set(name=cache_key, value=json.dumps(response))
        actual = cache_handler.get()
        assert actual == response

    def test_get__non_existing_key__returns_none(self, cache_handler: RedisSessionCacheHandler):
        actual = cache_handler.get()
        assert actual is None

    def test_set__inserts_value_returns_none(self,
                                             cache_handler: RedisSessionCacheHandler,
                                             redis: Redis,
                                             cache_key: str,
                                             response: Dict[str, str]):
        actual = cache_handler.set(response)

        assert actual is None
        self._assert_response_stored_under_key(
            redis=redis,
            response=response,
            cache_key=cache_key
        )

    @fixture
    def response(self) -> Dict[str, str]:
        return random_string_dict()

    @fixture
    def cache_key(self) -> str:
        return random_alphanumeric_string()

    @fixture
    def cache_handler(self, cache_key: str, redis: Redis) -> RedisSessionCacheHandler:
        return RedisSessionCacheHandler(
            key=cache_key,
            redis=redis
        )

    @fixture(scope="class")
    def redis(self) -> Redis:
        with RedisTestkit() as testkit:
            yield testkit.get_redis()

    @staticmethod
    def _assert_response_stored_under_key(redis: Redis,
                                          response: Dict[str, str],
                                          cache_key: str) -> None:
        cached_response = redis.get(cache_key)
        assert json.loads(cached_response) == response
