import pytest

from spotipyio.models import MatchingEntity


class TestMatchingEntity:
    def test_matching_entity__all_fields_missing__raises_value_error(self):
        with pytest.raises(ValueError):
            MatchingEntity()
