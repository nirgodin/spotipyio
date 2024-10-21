import os
from random import choice
from unittest.mock import patch

import pytest

from spotipyio.auth import ClientCredentials, SpotifyGrantType
from spotipyio.logic.consts.env_consts import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
from spotipyio.logic.utils import random_alphanumeric_string


class TestClientCredentials:
    def test_init__no_explicit_client_details_with_env_vars__creates_successfully_and_sets_env_var_as_attributes(self):
        mock_env_vars = {
            SPOTIPY_CLIENT_ID: random_alphanumeric_string(),
            SPOTIPY_CLIENT_SECRET: random_alphanumeric_string(),
            SPOTIPY_REDIRECT_URI: random_alphanumeric_string(),
        }

        with patch.dict(os.environ, mock_env_vars):
            credentials = ClientCredentials()

        assert credentials.client_id == mock_env_vars[SPOTIPY_CLIENT_ID]
        assert credentials.client_secret == mock_env_vars[SPOTIPY_CLIENT_SECRET]
        assert credentials.redirect_uri == mock_env_vars[SPOTIPY_REDIRECT_URI]

    def test_init__missing_client_details_without_env_var__raises_value_error(self):
        client_details = {
            "client_id": random_alphanumeric_string(),
            "client_secret": random_alphanumeric_string(),
            "redirect_uri": random_alphanumeric_string(),
        }
        self._randomly_pop_key(client_details)

        with pytest.raises(ValueError):
            ClientCredentials(**client_details)

    def test_init__missing_access_code_with_authorization_grant_type__raises_value_error(self):
        with pytest.raises(ValueError):
            ClientCredentials(
                client_id=random_alphanumeric_string(),
                client_secret=random_alphanumeric_string(),
                redirect_uri=random_alphanumeric_string(),
                grant_type=choice([SpotifyGrantType.AUTHORIZATION_CODE, SpotifyGrantType.REFRESH_TOKEN]),
                access_code=None,
            )

    @staticmethod
    def _randomly_pop_key(dct: dict) -> None:
        key = choice(list(dct.keys()))
        dct.pop(key)
