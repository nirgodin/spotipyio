from calendar import monthrange
from datetime import datetime
from random import randint, choice, random, uniform
from string import ascii_letters, digits
from typing import Optional, List, Dict, Callable, Any, Type

from spotipyio.consts.typing_consts import EnumType
from spotipyio.models import SearchItem, SearchItemFilters, SearchItemMetadata, SpotifySearchType
from spotipyio.consts.spotify_consts import PLAYLISTS, USERS, LIMIT, HREF, NEXT, OFFSET, TOTAL, ITEMS, ARTISTS, TRACKS, \
    ALBUMS, TRACK, AUDIO_FEATURES
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
    def paged_playlists(**kwargs) -> dict:
        entity_id = kwargs.get("id", SpotifyMockFactory.spotify_id())
        href = kwargs.get("href") or SpotifyMockFactory.href(
            entity_type=USERS,
            entity_id=entity_id,
            extra_routes=[PLAYLISTS]  # TODO: Improve
        )
        return {
            HREF: href,
            LIMIT: kwargs.get(LIMIT, randint(1, 50)),
            NEXT: "",  # TODO: Improve
            OFFSET: kwargs.get(OFFSET, randint(1, 200)),
            TOTAL: kwargs.get(TOTAL, randint(1, 1000)),
            ITEMS: kwargs.get(ITEMS, SpotifyMockFactory._some_playlists())
        }

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
            artists = [SpotifyMockFactory.artist(id=artist_id) for artist_id in ids]
        else:
            artists = SpotifyMockFactory._some_artists()

        return {ARTISTS: artists}

    @staticmethod
    def several_tracks(ids: Optional[List[str]] = None) -> Dict[str, List[dict]]:
        if ids:
            tracks = [SpotifyMockFactory.track(id=track_id) for track_id in ids]
        else:
            tracks = [SpotifyMockFactory.track() for _ in range(randint(1, 10))]

        return {TRACKS: tracks}

    @staticmethod
    def several_albums(ids: Optional[List[str]] = None) -> Dict[str, List[dict]]:
        if ids:
            albums = [SpotifyMockFactory.album(id=album_id) for album_id in ids]
        else:
            albums = [SpotifyMockFactory.album() for _ in range(randint(1, 10))]

        return {ALBUMS: albums}

    @staticmethod
    def several_audio_features(ids: Optional[List[str]] = None) -> Dict[str, List[dict]]:
        if ids:
            audio_features = [SpotifyMockFactory.audio_features(id=album_id) for album_id in ids]
        else:
            audio_features = [SpotifyMockFactory.audio_features() for _ in range(randint(1, 10))]

        return {AUDIO_FEATURES: audio_features}

    @staticmethod
    def artist(**kwargs) -> dict:
        entity_type = "artist"
        entity_id = kwargs.get("id") or SpotifyMockFactory.spotify_id()

        return {
            "external_urls": kwargs.get("external_urls") or SpotifyMockFactory.external_urls(entity_type, entity_id),
            "followers": kwargs.get("followers", SpotifyMockFactory.followers()),
            "genres": kwargs.get("genres", SpotifyMockFactory.genres()),
            "href": SpotifyMockFactory.href(entity_type, entity_id),
            "id": entity_id,
            "images": kwargs.get("images", SpotifyMockFactory.images()),
            "name": kwargs.get("name", SpotifyMockFactory.name()),
            "popularity": kwargs.get("popularity", SpotifyMockFactory.popularity()),
            "type": entity_type,
            "uri": SpotifyMockFactory.uri(entity_type=entity_type, entity_id=entity_id)
        }

    @staticmethod
    def track(**kwargs) -> dict:
        entity_id = kwargs.get("id", SpotifyMockFactory.spotify_id())
        entity_type = "track"
        artists = kwargs.get("artists", SpotifyMockFactory._some_artists())

        return {
            "album": kwargs.get("album", SpotifyMockFactory.album(artists=artists)),
            "artists": artists,
            "available_markets": kwargs.get("available_markets", SpotifyMockFactory.available_markets()),
            "disc_number": kwargs.get("disc_number", SpotifyMockFactory.disc_number()),
            "duration_ms": kwargs.get("duration_ms", SpotifyMockFactory.duration_ms()),
            "explicit": kwargs.get("explicit", SpotifyMockFactory._random_boolean()),
            "external_ids": kwargs.get("external_ids", SpotifyMockFactory.external_ids()),
            "external_urls": kwargs.get("external_urls") or SpotifyMockFactory.external_urls(entity_type, entity_id),
            "href": SpotifyMockFactory.href(entity_type=entity_type, entity_id=entity_id),
            "id": entity_id,
            "is_local": kwargs.get("is_local", SpotifyMockFactory._random_boolean()),
            "is_playable": kwargs.get("is_playable", SpotifyMockFactory._random_boolean()),
            "name": kwargs.get("name", SpotifyMockFactory.name()),
            "popularity": kwargs.get("popularity", SpotifyMockFactory.popularity()),
            "preview_url": kwargs.get("preview_url", SpotifyMockFactory.preview_url()),
            "track_number": kwargs.get("track_number", SpotifyMockFactory.track_number()),
            "type": entity_type,
            "uri": SpotifyMockFactory.uri(entity_type=entity_type, entity_id=entity_id)
        }

    @staticmethod
    def album(**kwargs) -> dict:
        entity_type = "album"
        entity_id = kwargs.get("id", SpotifyMockFactory.spotify_id())

        return {
            "artists": kwargs.get("artists", SpotifyMockFactory._some_artists()),
            "album_type": kwargs.get("album_type", SpotifyMockFactory.album_type()),
            "total_tracks": kwargs.get("total_tracks", SpotifyMockFactory.track_number()),
            "external_urls": SpotifyMockFactory.external_urls(entity_type=entity_type, entity_id=entity_id),
            "available_markets": kwargs.get("available_markets", SpotifyMockFactory.available_markets()),
            "href": SpotifyMockFactory.href(entity_type=entity_type, entity_id=entity_id),
            "id": entity_id,
            "images": kwargs.get("images", SpotifyMockFactory.images()),
            "name": kwargs.get("name", SpotifyMockFactory.name()),
            "release_date": kwargs.get("release_date", SpotifyMockFactory.release_date()),
            "release_date_precision": kwargs.get("release_date_precision", "day"),
            "type": entity_type,
            "uri": SpotifyMockFactory.uri(entity_type=entity_type, entity_id=entity_id),
            "is_playable": kwargs.get("is_playable", SpotifyMockFactory._random_boolean())
        }

    @staticmethod
    def audio_features(**kwargs) -> dict:
        entity_id = kwargs.get("id", SpotifyMockFactory.spotify_id())
        entity_type = TRACK

        return {
            "acousticness": SpotifyMockFactory._random_confidence("acousticness", **kwargs),
            "analysis_url": f"https://api.spotify.com/v1/audio-analysis/{entity_id}",
            "danceability": SpotifyMockFactory._random_confidence("danceability", **kwargs),
            "duration_ms": kwargs.get("duration_ms", randint(90000, 360000)),
            "energy": SpotifyMockFactory._random_confidence("energy", **kwargs),
            "id": entity_id,
            "instrumentalness": SpotifyMockFactory._random_confidence("instrumentalness", **kwargs),
            "key": kwargs.get("key", randint(0, 11)),
            "liveness": SpotifyMockFactory._random_confidence("liveness", **kwargs),
            "loudness": kwargs.get("loudness", randint(-60, 3)),
            "mode": kwargs.get("mode", SpotifyMockFactory._random_boolean()),
            "speechiness": SpotifyMockFactory._random_confidence("speechiness", **kwargs),
            "tempo": kwargs.get("tempo", uniform(40, 200)),
            "time_signature": kwargs.get("time_signature", randint(0, 5)),
            "track_href": SpotifyMockFactory.href(entity_type=entity_type, entity_id=entity_id),
            "type": "audio_features",
            "uri": SpotifyMockFactory.uri(entity_type=entity_type, entity_id=entity_id),
            "valence": SpotifyMockFactory._random_confidence("valence", **kwargs)
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
    def search_item() -> SearchItem:
        return SearchItem(
            text=SpotifyMockFactory._optional_random_alphanumeric_string(),
            filters=SearchItemFilters(
                track=SpotifyMockFactory._optional_random_alphanumeric_string(),
                artist=SpotifyMockFactory._optional_random_alphanumeric_string(),
                album=SpotifyMockFactory._optional_random_alphanumeric_string(),
                year=SpotifyMockFactory._an_optional(lambda: SpotifyMockFactory._random_datetime().year)
            ),
            metadata=SearchItemMetadata(
                search_types=SpotifyMockFactory._random_multi_enum_values(SpotifySearchType),
                quote=SpotifyMockFactory._random_boolean(),
            )
        )

    @staticmethod
    def search_response(search_types: List[SpotifySearchType]) -> Dict[str, dict]:
        search_types_method_mapping = {  # TODO: Support all methods
            SpotifySearchType.ALBUM: SpotifyMockFactory.several_albums,
            SpotifySearchType.TRACK: SpotifyMockFactory.several_tracks,
            SpotifySearchType.ARTIST: SpotifyMockFactory.several_artists,
        }
        response = {}

        for search_type in search_types:
            if search_type in search_types_method_mapping.keys():
                response_method = search_types_method_mapping[search_type]
                search_type_response = response_method()
                response.update(search_type_response)

        return response

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
    def _some_playlists() -> List[dict]:
        return [SpotifyMockFactory.playlist() for _ in range(randint(1, 10))]

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

    @staticmethod
    def _random_confidence(key: str, **kwargs) -> float:
        return kwargs.get(key, random())

    @staticmethod
    def _optional_random_alphanumeric_string() -> Optional[str]:
        return SpotifyMockFactory._an_optional(SpotifyMockFactory._random_alphanumeric_string)

    @staticmethod
    def _an_optional(value_generator: Callable[[], Any]) -> Optional[Any]:
        if SpotifyMockFactory._random_boolean():
            return value_generator()

    @staticmethod
    def _random_multi_enum_values(enum_: Type[EnumType]) -> List[EnumType]:
        return [v for v in enum_ if SpotifyMockFactory._random_boolean()]
