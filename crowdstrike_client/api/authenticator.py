# -*- coding: utf-8 -*-
"""CrowdStrike authenticator module."""

import logging
from typing import Dict, Mapping

from crowdstrike_client.api.utils import log_error_response
from crowdstrike_client.http.authenticator import (
    AbcAuthenticator,
    AuthenticatorException,
)
from crowdstrike_client.http.client import HTTPClient


class OAuth2Authenticator(AbcAuthenticator):
    """CrowdStrike OAuth2 authenticator."""

    _HEADER_ACCEPT = "Accept"
    _HEADER_CONTENT_TYPE = "Content-Type"
    _HEADER_AUTHORIZATION = "Authorization"

    _MIME_APPLICATION_JSON = "application/json"
    _MIME_APPLICATION_FORM_URL_ENCODED = "application/x-www-form-urlencoded"

    _DEFAULT_HEADERS = {
        _HEADER_ACCEPT: _MIME_APPLICATION_JSON,
        _HEADER_CONTENT_TYPE: _MIME_APPLICATION_FORM_URL_ENCODED,
    }

    _FROM_DATA_CLIENT_ID = "client_id"
    _FROM_DATA_CLIENT_SECRET = "client_secret"

    _JSON_ACCESS_TOKEN = "access_token"
    _JSON_TOKEN_TYPE = "token_type"
    _JSON_EXPIRES_IN = "expires_in"

    _TOKEN_ENDPOINT = "/oauth2/token"

    def __init__(self, client: HTTPClient, client_id: str, client_secret: str) -> None:
        """Initialize CrowdStrike OAuth2 authenticator."""
        self.log = logging.getLogger(__name__)

        self._client = client

        self._form_data = {
            self._FROM_DATA_CLIENT_ID: client_id,
            self._FROM_DATA_CLIENT_SECRET: client_secret,
        }

    def _get_request_headers(self) -> Mapping[str, str]:
        return self._DEFAULT_HEADERS.copy()

    def authenticate(self) -> Dict[str, str]:
        """Perform authentication."""
        path = self._TOKEN_ENDPOINT
        data = self._form_data
        headers = self._get_request_headers()

        response = self._client.post(path, data=data, headers=headers)

        status_code = response.status_code
        if status_code != 201:
            log_error_response(self.log, response)
            raise AuthenticatorException(f"Authentication failed ({status_code})")

        result = response.json()

        access_token = result[self._JSON_ACCESS_TOKEN]
        token_type = result[self._JSON_TOKEN_TYPE]
        expires_in = result[self._JSON_EXPIRES_IN]

        self.log.info(
            "Generated access token (type '%s') expires in %s seconds",
            token_type,
            expires_in,
        )

        return {self._HEADER_AUTHORIZATION: f"bearer {access_token}"}
