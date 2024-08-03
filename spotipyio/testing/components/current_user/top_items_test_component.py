from pytest_httpserver import RequestHandler

from spotipyio.consts.spotify_consts import TIME_RANGE, LIMIT
from spotipyio.logic.collectors.top_items_collectors.items_type import ItemsType
from spotipyio.logic.collectors.top_items_collectors.time_range import TimeRange
from spotipyio.testing.infra.base_test_component import BaseTestComponent


class TopItemsTestComponent(BaseTestComponent):
    def expect(self, items_type: ItemsType, time_range: TimeRange, limit: int = 50) -> RequestHandler:
        params = {
            TIME_RANGE: time_range.value,
            LIMIT: limit
        }
        return self._expect_get_request(
            route=f"/me/top/{items_type.value}",
            params=params,
        )
