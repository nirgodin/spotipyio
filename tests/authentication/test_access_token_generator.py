from enum import Enum
from typing import Dict

import pytest
from _pytest.fixtures import fixture
from pytest_httpserver import HTTPServer

from spotipyio.auth import SpotifyGrantType
from spotipyio.logic.authorization import AccessTokenGenerator
from spotipyio.logic.consts.api_consts import (
    GRANT_TYPE,
    JSON,
    CODE,
    REDIRECT_URI,
    REFRESH_TOKEN,
    CLIENT_ID,
    ACCESS_TOKEN,
    EXPIRES_IN,
    SCOPE,
    TOKEN_TYPE,
)
from spotipyio.logic.utils import encode_bearer_token, random_alphanumeric_string
from tests.testing_utils import build_request_data, random_string_array


class TestAccessTokenGenerator:
    async def test_generate__invalid_grant_type__raises_value_error(self, access_token_generator: AccessTokenGenerator):
        class MockGrantType(Enum):
            A = 1

        with pytest.raises(ValueError):
            await access_token_generator.generate(MockGrantType.A, None)

    async def test_generate__client_credentials(
        self,
        authorization_server: HTTPServer,
        expected_headers: Dict[str, str],
        access_token_generator: AccessTokenGenerator,
    ):
        expected = {"access_token": random_alphanumeric_string(), "token_type": "bearer", "expires_in": 3600}
        expected_payload = {GRANT_TYPE: SpotifyGrantType.CLIENT_CREDENTIALS.value, JSON: True}
        self._expect_successful_request(
            authorization_server=authorization_server,
            payload=expected_payload,
            headers=expected_headers,
            expected=expected,
        )

        actual = await access_token_generator.generate(grant_type=SpotifyGrantType.CLIENT_CREDENTIALS, access_code=None)

        assert actual == expected

    async def test_generate__authorization_code(
        self,
        redirect_uri: str,
        expected_headers: Dict[str, str],
        authorization_server: HTTPServer,
        access_token_generator: AccessTokenGenerator,
    ):
        access_code = random_alphanumeric_string()
        expected = self._random_authorization_response()
        expected_payload = {
            GRANT_TYPE: SpotifyGrantType.AUTHORIZATION_CODE.value,
            CODE: access_code,
            REDIRECT_URI: redirect_uri,
            JSON: True,
        }
        self._expect_successful_request(
            authorization_server=authorization_server,
            payload=expected_payload,
            headers=expected_headers,
            expected=expected,
        )

        actual = await access_token_generator.generate(
            grant_type=SpotifyGrantType.AUTHORIZATION_CODE, access_code=access_code
        )

        assert actual == expected

    async def test_generate__refresh_token(
        self,
        client_id: str,
        expected_headers: Dict[str, str],
        authorization_server: HTTPServer,
        access_token_generator: AccessTokenGenerator,
    ):
        refresh_token = random_alphanumeric_string()
        expected = self._random_authorization_response()
        expected_payload = {
            GRANT_TYPE: SpotifyGrantType.REFRESH_TOKEN.value,
            REFRESH_TOKEN: refresh_token,
            CLIENT_ID: client_id,
        }
        self._expect_successful_request(
            authorization_server=authorization_server,
            payload=expected_payload,
            headers=expected_headers,
            expected=expected,
        )

        actual = await access_token_generator.generate(
            grant_type=SpotifyGrantType.REFRESH_TOKEN, access_code=refresh_token
        )

        assert actual == expected

    @fixture(scope="class")
    def authorization_server(self) -> HTTPServer:
        with HTTPServer() as mock_authorization_server:
            yield mock_authorization_server

    @fixture(scope="class")
    def token_request_url(self, authorization_server: HTTPServer) -> str:
        return authorization_server.url_for("").rstrip("/")

    @fixture
    def client_details(self, client_id: str, client_secret: str, redirect_uri: str) -> Dict[str, str]:
        return {"client_id": client_id, "client_secret": client_secret, "redirect_uri": redirect_uri}

    @fixture
    def expected_headers(self, client_id: str, client_secret: str) -> Dict[str, str]:
        encoded_header = encode_bearer_token(client_id=client_id, client_secret=client_secret)
        return {"Authorization": f"Basic {encoded_header}"}

    @fixture
    async def access_token_generator(
        self, client_details: Dict[str, str], token_request_url: str
    ) -> AccessTokenGenerator:
        async with AccessTokenGenerator(token_request_url, **client_details) as access_token_generator:
            yield access_token_generator

    @staticmethod
    def _expect_successful_request(
        authorization_server: HTTPServer, payload: Dict[str, str], headers: Dict[str, str], expected: dict
    ) -> None:
        request_handler = authorization_server.expect_request(
            method="POST", uri="/", data=build_request_data(payload), headers=headers
        )
        request_handler.respond_with_json(expected)

    @staticmethod
    def _random_authorization_response() -> dict:
        return {
            ACCESS_TOKEN: random_alphanumeric_string(),
            TOKEN_TYPE: "bearer",
            SCOPE: ",".join(random_string_array()),
            EXPIRES_IN: 3600,
            REFRESH_TOKEN: random_alphanumeric_string(),
        }
