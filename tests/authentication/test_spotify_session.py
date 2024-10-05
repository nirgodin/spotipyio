from random import choice
from typing import Dict, Optional
from unittest.mock import AsyncMock, MagicMock

import pytest
from _pytest.fixtures import fixture

from spotipyio import SpotifySession
from spotipyio.logic.consts.api_consts import REFRESH_TOKEN, ACCESS_TOKEN
from spotipyio.auth import SpotifyGrantType, ISessionCacheHandler
from spotipyio.logic.authorization import AccessTokenGenerator
from spotipyio.logic.utils import create_client_session
from tests.testing_utils import random_alphanumeric_string, an_optional, random_string_dict


class TestSpotifySession:
    async def test_aenter__with_cached_response__creates_headers_using_refresh_request_and_caches_response(
        self,
        session: SpotifySession,
        mock_cache_handler: MagicMock,
        refresh_token: str,
        refreshed_access_token: str,
        mock_token_generator: AsyncMock,
    ):
        self._given_cached_response_is(mock_cache_handler, cached_response={REFRESH_TOKEN: refresh_token})

        async with session as spotify_session:
            mock_token_generator.generate.assert_called_once_with(
                grant_type=SpotifyGrantType.REFRESH_TOKEN, access_code=refresh_token
            )
            self._assert_expected_bearer_token(session=spotify_session, expected=refreshed_access_token)
            self._assert_expected_response_cached(cache_handler=mock_cache_handler, expected=refreshed_access_token)

    async def test_aenter__no_cached_response__creates_headers_using_token_request_and_caches_response(
        self,
        session: SpotifySession,
        mock_cache_handler: MagicMock,
        grant_type: SpotifyGrantType,
        access_code: str,
        regular_access_token: str,
        mock_token_generator: AsyncMock,
    ):
        self._given_cached_response_is(mock_cache_handler, cached_response=None)

        async with session as spotify_session:
            mock_token_generator.generate.assert_called_once_with(grant_type=grant_type, access_code=access_code)
            self._assert_expected_bearer_token(session=spotify_session, expected=regular_access_token)
            self._assert_expected_response_cached(cache_handler=mock_cache_handler, expected=regular_access_token)

    async def test_aenter__no_cache_handler__creates_headers_using_token_request(
        self,
        session_without_cache: SpotifySession,
        mock_cache_handler: MagicMock,
        grant_type: SpotifyGrantType,
        access_code: str,
        regular_access_token: str,
        mock_token_generator: AsyncMock,
    ):
        async with session_without_cache as spotify_session:
            mock_token_generator.generate.assert_called_once_with(grant_type=grant_type, access_code=access_code)
            self._assert_expected_bearer_token(session=spotify_session, expected=regular_access_token)
            mock_cache_handler.set.assert_not_called()

    async def test_aenter__existing_client_session__doesnt_generate_new_token(self, mock_token_generator: AsyncMock):
        bearer_token = random_alphanumeric_string()
        headers = {"Authorization": f"Bearer {bearer_token}"}
        client_session = create_client_session(headers)

        async with SpotifySession(session=client_session, access_token_generator=mock_token_generator) as session:
            mock_token_generator.generate.assert_not_called()
            self._assert_expected_bearer_token(session=session, expected=bearer_token)

    async def test_refresh__no_cache_handler__creates_headers_using_token_request(
        self,
        session_without_cache: SpotifySession,
        mock_cache_handler: MagicMock,
        grant_type: SpotifyGrantType,
        access_code: str,
        regular_access_token: str,
        mock_token_generator: AsyncMock,
    ):
        await session_without_cache.refresh()

        mock_token_generator.generate.assert_called_once_with(grant_type=grant_type, access_code=access_code)
        self._assert_expected_bearer_token(session=session_without_cache, expected=regular_access_token)
        mock_cache_handler.set.assert_not_called()

    @pytest.mark.parametrize("cached_response", [None, random_string_dict()])
    async def test_refresh__with_cached_response__creates_headers_using_token_request_and_caches_response(
        self,
        cached_response: Optional[Dict[str, str]],
        session: SpotifySession,
        mock_cache_handler: MagicMock,
        grant_type: SpotifyGrantType,
        access_code: str,
        regular_access_token: str,
        mock_token_generator: AsyncMock,
    ):
        self._given_cached_response_is(mock_cache_handler, cached_response=cached_response)

        await session.refresh()

        mock_token_generator.generate.assert_called_once_with(grant_type=grant_type, access_code=access_code)
        self._assert_expected_bearer_token(session=session, expected=regular_access_token)
        self._assert_expected_response_cached(cache_handler=mock_cache_handler, expected=regular_access_token)

    @fixture
    def grant_type(self) -> SpotifyGrantType:
        return choice([SpotifyGrantType.CLIENT_CREDENTIALS, SpotifyGrantType.AUTHORIZATION_CODE])

    @fixture
    def access_code(self) -> Optional[str]:
        return an_optional(random_alphanumeric_string)

    @fixture
    async def session(
        self,
        mock_token_generator: AsyncMock,
        mock_cache_handler: MagicMock,
        grant_type: SpotifyGrantType,
        access_code: str,
    ) -> SpotifySession:
        session = SpotifySession(
            access_token_generator=mock_token_generator,
            session_cache_handler=mock_cache_handler,
            grant_type=grant_type,
            access_code=access_code,
        )
        yield session
        await session.stop()

    @fixture
    async def session_without_cache(
        self, mock_token_generator: AsyncMock, grant_type: SpotifyGrantType, access_code: str
    ) -> SpotifySession:
        session = SpotifySession(
            access_token_generator=mock_token_generator, grant_type=grant_type, access_code=access_code
        )
        yield session
        await session.stop()

    @fixture
    def mock_token_generator(self, refreshed_access_token: str, regular_access_token: str) -> AsyncMock:
        def _mock_generate(grant_type: SpotifyGrantType, access_code: Optional[str]) -> Dict[str, str]:
            if grant_type == SpotifyGrantType.REFRESH_TOKEN:
                access_token = refreshed_access_token
            else:
                access_token = regular_access_token

            return {ACCESS_TOKEN: access_token}

        token_generator = AsyncMock(AccessTokenGenerator)
        token_generator.generate.side_effect = _mock_generate

        return token_generator

    @fixture
    def refresh_token(self) -> str:
        return random_alphanumeric_string()

    @fixture
    def refreshed_access_token(self) -> str:
        return random_alphanumeric_string()

    @fixture
    def regular_access_token(self) -> str:
        return random_alphanumeric_string()

    @fixture
    def mock_cache_handler(self) -> MagicMock:
        return MagicMock(ISessionCacheHandler)

    @staticmethod
    def _given_cached_response_is(mock_cache_handler: MagicMock, cached_response: Optional[Dict[str, str]]) -> None:
        mock_cache_handler.get.return_value = cached_response

    @staticmethod
    def _assert_expected_bearer_token(session: SpotifySession, expected: str) -> None:
        headers = session.get_authorization_headers()
        actual = headers["Authorization"]
        assert actual == f"Bearer {expected}"

    @staticmethod
    def _assert_expected_response_cached(cache_handler: AsyncMock, expected: str) -> None:
        cache_handler.set.assert_called_once_with({ACCESS_TOKEN: expected})
