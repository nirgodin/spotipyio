import pytest
from _pytest.fixtures import fixture

from spotipyio.models import SearchItem, SearchItemFilters, SearchItemMetadata, SpotifySearchType


class TestSearchItem:
    def test_search_item__no_text_and_all_filters_missing__raises_value_error(self):
        with pytest.raises(ValueError):
            SearchItem()

    def test_to_query_params__quote_false__returns_non_encoded_params_dict(self, search_item: SearchItem):
        expected = {"q": "Bridge Over Troubled Water artist:Simon & Garfunkel year:1970", "type": "track,album"}
        actual = search_item.to_query_params()
        assert actual == expected

    def test_to_query_params__quote_true__returns_encoded_params_dict(self, search_item: SearchItem):
        search_item.metadata.quote = True
        expected = {
            "q": "Bridge%20Over%20Troubled%20Water%20artist%3ASimon%20%26%20Garfunkel%20year%3A1970",
            "type": "track,album",
        }

        actual = search_item.to_query_params()

        assert actual == expected

    def test_to_query_params__text_none__includes_only_filters_in_query(self, search_item: SearchItem):
        search_item.text = None
        expected = {"q": "artist:Simon & Garfunkel year:1970", "type": "track,album"}

        actual = search_item.to_query_params()

        assert actual == expected

    def test_to_query_params__no_filters__includes_only_text_in_query(self, search_item: SearchItem):
        search_item.filters = SearchItemFilters()
        expected = {"q": "Bridge Over Troubled Water", "type": "track,album"}

        actual = search_item.to_query_params()

        assert actual == expected

    @fixture
    def search_item(self) -> SearchItem:
        return SearchItem(
            text="Bridge Over Troubled Water",
            filters=SearchItemFilters(artist="Simon & Garfunkel", year=1970),
            metadata=SearchItemMetadata(search_types=[SpotifySearchType.TRACK, SpotifySearchType.ALBUM], quote=False),
        )
