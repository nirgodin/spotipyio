from enum import Enum


class ChunkSize(Enum):
    ALBUMS = 20
    ARTISTS = 50
    AUDIO_FEATURES = 100
    ITEMS_ADDITION = 100
    ITEMS_REMOVAL = 100
    TRACKS = 50