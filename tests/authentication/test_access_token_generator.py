import os
from random import choice
from typing import Dict
from unittest.mock import patch

import pytest
from _pytest.fixtures import fixture

from spotipyio import AccessTokenGenerator
from spotipyio.consts.env_consts import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
from tests.testing_utils import random_alphanumeric_string


class TestAccessTokenGenerator:
    async def test_init__no_explicit_client_details_with_env_vars__creates_successfully(self, token_request_url: str):
        mock_env_vars = {
            SPOTIPY_CLIENT_ID: random_alphanumeric_string(),
            SPOTIPY_CLIENT_SECRET: random_alphanumeric_string(),
            SPOTIPY_REDIRECT_URI: random_alphanumeric_string()
        }

        with patch.dict(os.environ, mock_env_vars):
            AccessTokenGenerator(token_request_url)

    async def test_init__missing_client_details_without_env_var__raises_key_error(self,
                                                                                  client_details: Dict[str, str],
                                                                                  token_request_url: str):
        self._randomly_pop_key(client_details)

        with pytest.raises(KeyError):
            AccessTokenGenerator(token_request_url, **client_details)

    @fixture
    def client_details(self) -> Dict[str, str]:
        return {
            "client_id": random_alphanumeric_string(),
            "client_secret": random_alphanumeric_string(),
            "redirect_uri": random_alphanumeric_string()
        }

    @fixture
    def access_token_generator(self, client_details: Dict[str, str], token_request_url: str) -> AccessTokenGenerator:
        return AccessTokenGenerator(
            token_request_url=token_request_url,
            **client_details
        )

    @staticmethod
    def _randomly_pop_key(dct: dict) -> None:
        key = choice(list(dct.keys()))
        dct.pop(key)
