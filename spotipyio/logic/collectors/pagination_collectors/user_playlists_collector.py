from typing import Optional

from spotipyio.consts.spotify_consts import SPOTIFY_USERS_BASE_URL, NEXT, ITEMS
from spotipyio.contract import BasePaginationCollector


class UserPlaylistsCollector(BasePaginationCollector):
    @property
    def _url_format(self) -> str:
        return f"{SPOTIFY_USERS_BASE_URL}/{{id}}/playlists?offset=0&limit=50"

    @property
    def _additional_items_request_params(self) -> None:
        return None

    def _extract_first_next_url(self, result: dict) -> Optional[str]:
        return result[NEXT]

    def _extract_subsequent_next_url(self, page: dict) -> Optional[str]:
        return page[NEXT]

    def _extend_existing_items(self, result: dict, page: dict) -> None:
        existing_items = result[ITEMS]
        page_items = page[ITEMS]
        existing_items.extend(page_items)
