from calendar import monthrange
from datetime import datetime
from random import randint, choice
from string import ascii_letters, digits
from typing import Optional, List, Dict

from spotipyio.logic.collectors.top_items_collectors.items_type import ItemsType


class SpotifyMockFactory:
    @staticmethod
    def spotify_id() -> str:
        return SpotifyMockFactory._random_alphanumeric_string(min_length=22, max_length=22)

    @staticmethod
    def some_spotify_ids(length: Optional[int] = None) -> List[str]:
        number_of_ids = length or randint(2, 10)
        return [SpotifyMockFactory.spotify_id() for _ in range(number_of_ids)]

    @staticmethod
    def playlist(user_id: Optional[str] = None, **kwargs) -> dict:
        owner = kwargs.get("owner", SpotifyMockFactory.owner(user_id))
        entity_type = "playlist"
        entity_id = kwargs.get("id", SpotifyMockFactory.spotify_id())

        return {
            "collaborative": kwargs.get("collaborative", SpotifyMockFactory._random_boolean()),
            "description": kwargs.get("description", SpotifyMockFactory._random_alphanumeric_string()),
            "external_urls": SpotifyMockFactory.external_urls(entity_type=entity_type, entity_id=entity_id),
            "followers": kwargs.get("followers", SpotifyMockFactory.followers()),
            "href": SpotifyMockFactory.href(entity_type=entity_type, entity_id=entity_id),
            "id": entity_id,
            "images": kwargs.get("images", SpotifyMockFactory.images()),
            "name": kwargs.get("name", SpotifyMockFactory.name()),
            "owner": owner,
            "public": kwargs.get("public", SpotifyMockFactory._random_boolean()),
            "snapshot_id": kwargs.get("snapshot_id", SpotifyMockFactory.snapshot_id()),
            "tracks": kwargs.get("tracks", SpotifyMockFactory.playlist_tracks(entity_id=entity_id, owner=owner)),
            "type": entity_type,
            "uri": SpotifyMockFactory.uri(entity_type=entity_type, entity_id=entity_id),
            "primary_color": None
        }

    @staticmethod
    def playlist_tracks(entity_id: Optional[str] = None, owner: Optional[dict] = None) -> dict:
        entity_type = "playlist"
        if entity_id is None:
            entity_id = SpotifyMockFactory.spotify_id()

        total_tracks = randint(1, 10)
        items = [SpotifyMockFactory.playlist_item(owner) for _ in range(total_tracks)]

        return {
            "href": SpotifyMockFactory.href(entity_type=entity_type, entity_id=entity_id, extra_routes=["tracks"]),
            "limit": 100,
            "next": None,
            "offset": 0,
            "previous": None,
            "total": total_tracks,
            "items": items
        }

    @staticmethod
    def playlist_item(owner: Optional[str] = None) -> dict:
        added_at = SpotifyMockFactory._random_datetime()
        return {
            "added_at": added_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "added_by": owner or SpotifyMockFactory.owner(),
            "is_local": SpotifyMockFactory._random_boolean(),
            "track": SpotifyMockFactory.track()
        }

    @staticmethod
    def snapshot_id() -> str:
        return SpotifyMockFactory._random_alphanumeric_string(min_length=32, max_length=32)

    @staticmethod
    def owner(entity_id: Optional[str] = None) -> dict:
        entity_type = "user"
        if entity_id is None:
            entity_id = SpotifyMockFactory._random_alphanumeric_string()

        return {
            "external_urls": SpotifyMockFactory.external_urls(entity_type=entity_type, entity_id=entity_id),
            "href": SpotifyMockFactory.href(entity_type=entity_type, entity_id=entity_id),
            "id": entity_id,
            "type": entity_type,
            "uri": SpotifyMockFactory.uri(entity_type=entity_type, entity_id=entity_id),
            "display": SpotifyMockFactory._random_alphanumeric_string()
        }

    @staticmethod
    def several_artists(ids: Optional[List[str]] = None) -> Dict[str, List[dict]]:
        if ids:
            artists = [SpotifyMockFactory.artist(artist_id) for artist_id in ids]
        else:
            artists = SpotifyMockFactory._some_artists()

        return {"artists": artists}

    @staticmethod
    def several_tracks(ids: Optional[List[str]] = None) -> Dict[str, List[dict]]:
        if ids:
            tracks = [SpotifyMockFactory.track(track_id) for track_id in ids]
        else:
            tracks = [SpotifyMockFactory.track() for _ in range(randint(1, 10))]

        return {"tracks": tracks}

    @staticmethod
    def artist(entity_id: Optional[str] = None) -> dict:
        entity_type = "artist"
        if entity_id is None:
            entity_id = SpotifyMockFactory.spotify_id()

        return {
            "external_urls": SpotifyMockFactory.external_urls(entity_type=entity_type, entity_id=entity_id),
            "followers": SpotifyMockFactory.followers(),
            "genres": SpotifyMockFactory.genres(),
            "href": SpotifyMockFactory.href(entity_type=entity_type, entity_id=entity_id),
            "id": entity_id,
            "images": SpotifyMockFactory.images(),
            "name": SpotifyMockFactory.name(),
            "popularity": SpotifyMockFactory.popularity(),
            "type": entity_type,
            "uri": SpotifyMockFactory.uri(entity_type=entity_type, entity_id=entity_id)
        }

    @staticmethod
    def track(entity_id: Optional[str] = None) -> dict:
        if entity_id is None:
            entity_id = SpotifyMockFactory.spotify_id()

        entity_type = "track"
        artists = SpotifyMockFactory._some_artists()

        return {
            "album": SpotifyMockFactory.album(artists=artists),
            "artists": artists,
            "available_markets": SpotifyMockFactory.available_markets(),
            "disc_number": SpotifyMockFactory.disc_number(),
            "duration_ms": SpotifyMockFactory.duration_ms(),
            "explicit": SpotifyMockFactory._random_boolean(),
            "external_ids": SpotifyMockFactory.external_ids(),
            "external_urls": SpotifyMockFactory.external_urls(entity_type=entity_type, entity_id=entity_id),
            "href": SpotifyMockFactory.href(entity_type=entity_type, entity_id=entity_id),
            "id": entity_id,
            "is_local": SpotifyMockFactory._random_boolean(),
            "is_playable": SpotifyMockFactory._random_boolean(),
            "name": SpotifyMockFactory.name(),
            "popularity": SpotifyMockFactory.popularity(),
            "preview_url": SpotifyMockFactory.preview_url(),
            "track_number": SpotifyMockFactory.track_number(),
            "type": entity_type,
            "uri": SpotifyMockFactory.uri(entity_type=entity_type, entity_id=entity_id)
        }

    @staticmethod
    def album(entity_id: Optional[str] = None, artists: Optional[List[dict]] = None) -> dict:
        entity_type = "album"
        if entity_id is None:
            entity_id = SpotifyMockFactory.spotify_id()

        return {
            "artists": artists or SpotifyMockFactory._some_artists(),
            "album_type": SpotifyMockFactory.album_type(),
            "total_tracks": SpotifyMockFactory.track_number(),
            "external_urls": SpotifyMockFactory.external_urls(entity_type=entity_type, entity_id=entity_id),
            "available_markets": SpotifyMockFactory.available_markets(),
            "href": SpotifyMockFactory.href(entity_type=entity_type, entity_id=entity_id),
            "id": entity_id,
            "images": SpotifyMockFactory.images(),
            "name": SpotifyMockFactory.name(),
            "release_date": SpotifyMockFactory.release_date(),
            "release_date_precision": "day",
            "type": entity_type,
            "uri": SpotifyMockFactory.uri(entity_type=entity_type, entity_id=entity_id),
            "is_playable": SpotifyMockFactory._random_boolean()
        }

    @staticmethod
    def album_type() -> str:
        return choice(["album", "single", "compilation"])

    @staticmethod
    def available_markets() -> List[str]:
        return SpotifyMockFactory._random_string_array()

    @staticmethod
    def disc_number() -> int:
        return randint(1, 2)

    @staticmethod
    def duration_ms() -> int:
        return randint(90000, 360000)

    @staticmethod
    def external_urls(entity_type: str, entity_id: str) -> Dict[str, str]:
        return {"spotify": f"https://open.spotify.com/{entity_type}/{entity_id}"}

    @staticmethod
    def external_ids() -> Dict[str, str]:
        return {"isrc": SpotifyMockFactory._random_alphanumeric_string()}

    @staticmethod
    def href(entity_type: str, entity_id: str, extra_routes: Optional[List[str]] = None) -> str:
        href = f"https://api.spotify.com/v1/{entity_type}/{entity_id}"

        if extra_routes:
            formatted_routes = [route.strip("/") for route in extra_routes]
            joined_route = "/".join(formatted_routes)
            href += f"/{joined_route}"

        return href

    @staticmethod
    def followers(number: Optional[int] = None) -> dict:
        followers_number = number or randint(500, 50000000)
        return {
            "href": None,
            "total": followers_number
        }

    @staticmethod
    def genres(length: Optional[int] = None) -> List[str]:
        genres_number = length or randint(0, 5)
        return SpotifyMockFactory._random_string_array(genres_number)

    @staticmethod
    def images() -> List[Dict[str, str]]:
        return [SpotifyMockFactory._random_image(size) for size in [640, 320, 160]]

    @staticmethod
    def name() -> str:
        return SpotifyMockFactory._random_alphanumeric_string()

    @staticmethod
    def popularity() -> int:
        return randint(0, 100)

    @staticmethod
    def preview_url() -> str:
        return f"https://p.scdn.co/mp3-preview/{SpotifyMockFactory._random_alphanumeric_string()}"

    @staticmethod
    def release_date() -> str:
        raw_date = SpotifyMockFactory._random_datetime()
        return raw_date.strftime("%Y-%m-%d")

    @staticmethod
    def track_number() -> int:
        return randint(1, 20)

    @staticmethod
    def uri(entity_type: str, entity_id: str) -> str:
        return f"spotify:{entity_type}:{entity_id}"

    @staticmethod
    def some_uris(entity_type: str, length: Optional[int] = None) -> List[str]:
        number_of_uris = length or randint(2, 10)
        uris = []

        for _ in range(number_of_uris):
            uri = SpotifyMockFactory.uri(entity_type=entity_type, entity_id=SpotifyMockFactory.spotify_id())
            uris.append(uri)

        return uris

    @staticmethod
    def user_profile(entity_id: Optional[str] = None) -> dict:
        entity_type = "user"
        if entity_id is None:
            entity_id = SpotifyMockFactory.spotify_id()

        return {
            "country": SpotifyMockFactory._random_alphanumeric_string(),
            "display_name": SpotifyMockFactory._random_alphanumeric_string(),
            "email": SpotifyMockFactory._random_alphanumeric_string(),
            "explicit_content": {
                "filter_enabled": SpotifyMockFactory._random_boolean(),
                "filter_locked": SpotifyMockFactory._random_boolean()
            },
            "external_urls": SpotifyMockFactory.external_urls(entity_type=entity_type, entity_id=entity_id),
            "followers": SpotifyMockFactory.followers(),
            "href": SpotifyMockFactory.href(entity_type=entity_type, entity_id=entity_id),
            "id": entity_id,
            "images": SpotifyMockFactory.images(),
            "product": choice(["premium", "free"]),
            "type": entity_type,
            "uri": SpotifyMockFactory.uri(entity_type=entity_type, entity_id=entity_id)
        }

    @staticmethod
    def user_top_items(items_type: ItemsType) -> dict:
        total_tracks = randint(1, 10)
        href = SpotifyMockFactory.href(
            entity_type="me",
            entity_id="",
            extra_routes=["top", items_type.value]
        )

        if items_type == ItemsType.ARTISTS:
            items = SpotifyMockFactory._some_artists()
        else:
            items = SpotifyMockFactory._some_tracks()

        return {
            "href": href,
            "limit": 50,
            "next": None,
            "offset": 0,
            "previous": None,
            "total": total_tracks,
            "items": items
        }

    @staticmethod
    def _random_image(size: int) -> dict:
        image_id = SpotifyMockFactory._random_alphanumeric_string(min_length=40, max_length=40)
        return {
            "url": f"https://i.scdn.co/image/{image_id}",
            "height": size,
            "width": size
        }

    @staticmethod
    def _some_artists() -> List[dict]:
        return [SpotifyMockFactory.artist() for _ in range(randint(1, 10))]

    @staticmethod
    def _some_tracks() -> List[dict]:
        return [SpotifyMockFactory.track() for _ in range(randint(1, 10))]

    @staticmethod
    def _random_string_array(length: Optional[int] = None) -> List[str]:
        n_elements = length or randint(0, 10)
        return [SpotifyMockFactory._random_alphanumeric_string() for _ in range(n_elements)]

    @staticmethod
    def _random_alphanumeric_string(min_length: int = 1, max_length: int = 20) -> str:
        n_chars = randint(min_length, max_length)
        characters = ascii_letters + digits

        return ''.join(choice(characters) for _ in range(n_chars))

    @staticmethod
    def _random_boolean() -> bool:
        return choice([True, False])

    @staticmethod
    def _random_datetime() -> datetime:
        current_year = datetime.now().year
        year = randint(1950, current_year)
        month = randint(1, 12)
        _, last_month_day = monthrange(year, month)
        day = randint(1, last_month_day)

        return datetime(year, month, day)
