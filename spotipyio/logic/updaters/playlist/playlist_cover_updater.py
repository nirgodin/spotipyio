import os.path
from base64 import b64encode
from io import BytesIO
from tempfile import TemporaryDirectory
from typing import Dict

from spotipyio.consts.image_consts import RGB, JPG_FILE_SUFFIX
from spotipyio.consts.spotify_consts import IMAGES
from spotipyio.contract.updaters.base_playlist_updater import BasePlaylistsUpdater
from PIL import Image

from spotipyio.utils.datetime_utils import get_current_timestamp


class PlaylistCoverUpdater(BasePlaylistsUpdater):
    async def run(self, playlist_id: str, image: bytes) -> Dict[str, str]:
        url = self._build_url(playlist_id)
        data = self._convert_image_to_base64_jpeg(image)

        return await self._session.put(url=url, data=data)

    @property
    def _route(self) -> str:
        return IMAGES

    def _convert_image_to_base64_jpeg(self, image: bytes) -> str:
        image_io = BytesIO(image)
        image = Image.open(image_io)
        rgb_image = image.convert(RGB)

        with TemporaryDirectory() as dir_path:
            image_path = self._save_image_as_jpeg(rgb_image, dir_path)
            return self._encode_image_to_base64(image_path)

    @staticmethod
    def _save_image_as_jpeg(image: Image, dir_path: str) -> str:
        timestamp = get_current_timestamp()
        file_name = f"{timestamp}.{JPG_FILE_SUFFIX}"
        output_path = os.path.join(dir_path, file_name)
        image.save(output_path)

        return output_path

    @staticmethod
    def _encode_image_to_base64(image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            raw_image = image_file.read()
            encoded_image = b64encode(raw_image)

        return encoded_image.decode("utf-8")
