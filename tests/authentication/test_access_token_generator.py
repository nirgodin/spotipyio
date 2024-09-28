import os
from enum import Enum
from random import choice
from typing import Dict
from unittest.mock import patch

import pytest
from _pytest.fixtures import fixture
from pytest_httpserver import HTTPServer

from spotipyio import AccessTokenGenerator, SpotifyGrantType
from spotipyio.consts.api_consts import GRANT_TYPE, JSON, CODE, REDIRECT_URI
from spotipyio.consts.env_consts import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
from tests.testing_utils import random_alphanumeric_string, build_request_data, random_string_array, \
    random_localhost_url


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

    async def test_generate__invalid_grant_type__raises_value_error(self, access_token_generator: AccessTokenGenerator):
        class MockGrantType(Enum):
            A = 1

        with pytest.raises(ValueError):
            await access_token_generator.generate(MockGrantType.A, None)

    async def test_generate__client_credentials__returns_server_response(self,
                                                                         authorization_server: HTTPServer,
                                                                         access_token_generator: AccessTokenGenerator):
        expected = {
            "access_token": random_alphanumeric_string(),
            "token_type": "bearer",
            "expires_in": 3600
        }
        payload = {
            GRANT_TYPE: SpotifyGrantType.CLIENT_CREDENTIALS.value,
            JSON: True
        }
        self._expect_successful_request(
            authorization_server=authorization_server,
            payload=payload,
            expected=expected
        )

        actual = await access_token_generator.generate(grant_type=SpotifyGrantType.CLIENT_CREDENTIALS, access_code=None)

        assert actual == expected

    async def test_generate__authorization_code__returns_server_response(self,
                                                                         redirect_uri: str,
                                                                         authorization_server: HTTPServer,
                                                                         access_token_generator: AccessTokenGenerator):
        access_code = random_alphanumeric_string()
        expected = {
            "access_token": random_alphanumeric_string(),
            "token_type": "bearer",
            "scope": ",".join(random_string_array()),
            "expires_in": 3600,
            "refresh_token": random_alphanumeric_string()
        }
        payload = {
            GRANT_TYPE: SpotifyGrantType.AUTHORIZATION_CODE.value,
            CODE: access_code,
            REDIRECT_URI: redirect_uri,
            JSON: True
        }
        self._expect_successful_request(
            authorization_server=authorization_server,
            payload=payload,
            expected=expected
        )

        actual = await access_token_generator.generate(
            grant_type=SpotifyGrantType.AUTHORIZATION_CODE,
            access_code=access_code
        )

        assert actual == expected

    @fixture
    def redirect_uri(self) -> str:
        return random_localhost_url()

    @fixture
    def client_id(self) -> str:
        return random_alphanumeric_string(32, 32)

    @fixture
    def client_details(self, client_id: str, redirect_uri: str) -> Dict[str, str]:
        return {
            "client_id": client_id,
            "client_secret": random_alphanumeric_string(),
            "redirect_uri": redirect_uri
        }

    @fixture
    async def access_token_generator(self, client_details: Dict[str, str],
                                     token_request_url: str) -> AccessTokenGenerator:
        async with AccessTokenGenerator(token_request_url, **client_details) as access_token_generator:
            yield access_token_generator

    @staticmethod
    def _randomly_pop_key(dct: dict) -> None:
        key = choice(list(dct.keys()))
        dct.pop(key)

    @staticmethod
    def _expect_successful_request(authorization_server: HTTPServer,
                                   payload: Dict[str, str],
                                   expected: dict) -> None:
        request_handler = authorization_server.expect_request(
            method="POST",
            uri="/",
            data=build_request_data(payload)
        )
        request_handler.respond_with_json(expected)
