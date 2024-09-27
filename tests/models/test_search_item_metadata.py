import pytest

from spotipyio.models import SearchItemMetadata
from tests.testing_utils import random_boolean


class TestSearchItemMetadata:
    def test_search_item_metadata__no_search_types__raises_value_error(self):
        with pytest.raises(ValueError):
            SearchItemMetadata(
                search_types=[],
                quote=random_boolean()
            )
