# -*- coding: utf-8 -*-
"""HTTP client module."""

import logging
from typing import Any, Dict, Mapping, Optional

import requests

from crowdstrike_client.http.authenticator import AbcAuthenticator
from crowdstrike_client.http.exceptions import HTTPClientException


class HTTPClient:
    """HTTP client"""

    _ARG_HEADERS = "headers"
    _ARG_TIMEOUT = "timeout"

    _DEFAULT_TIMEOUT_CONNECT_SEC = 15
    _DEFAULT_TIMEOUT_READ_SEC = 120

    _DEFAULT_TIMEOUTS = (_DEFAULT_TIMEOUT_CONNECT_SEC, _DEFAULT_TIMEOUT_READ_SEC)

    def __init__(
        self, base_url: str, default_headers: Optional[Dict[str, str]] = None
    ) -> None:
        """Initialize HTTP client."""
        self.log = logging.getLogger(__name__)

        self._base_url = base_url if not base_url.endswith("/") else base_url[:-1]
        self._default_headers = default_headers

    def _get_url(self, path):
        return self._base_url + path

    def _get_request_headers(
        self, headers: Optional[Mapping[str, str]]
    ) -> Optional[Mapping[str, str]]:
        if self._default_headers is None:
            return headers

        if headers is None:
            new_headers = self._default_headers.copy()
        else:
            new_headers = self._default_headers.copy()
            new_headers.update(headers)

        return new_headers

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        self.log.debug(
            "_request method: %s, path: %s, kwargs: %s", method, path, kwargs
        )

        url = self._get_url(path)

        timeout = kwargs.pop(self._ARG_TIMEOUT, None)
        if timeout is None:
            timeout = self._DEFAULT_TIMEOUTS

        request_headers = kwargs.pop(self._ARG_HEADERS, None)
        request_headers = self._get_request_headers(request_headers)

        self.log.debug(
            "_request url: %s, request_headers: %s, timeout: %s, kwargs: %s",
            url,
            request_headers,
            timeout,
            kwargs,
        )

        response = requests.request(
            method, url, headers=request_headers, timeout=timeout, **kwargs
        )

        self.log.debug(
            "_request response status code: %s, response_headers: %s",
            response.status_code,
            response.headers,
        )

        return response

    def get(
        self,
        path: str,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> requests.Response:
        """Send HTTP GET request."""
        return self._request("GET", path, params=params, headers=headers)

    def post(
        self,
        path: str,
        data: Optional[Mapping[str, str]] = None,
        json: Optional[Any] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> requests.Response:
        """Send HTTP POST request."""
        return self._request("POST", path, data=data, json=json, headers=headers)


class AuthenticatedHTTPClient(HTTPClient):
    """Authenticated HTTP client."""

    def __init__(self, base_url: str, authenticator: AbcAuthenticator) -> None:
        """Initialize authenticated HTTP client"""
        super().__init__(base_url)
        self.log = logging.getLogger(__name__)

        self._authenticator = authenticator
        self._authorization: Optional[Dict[str, str]] = None

    def _check_authorization(self) -> None:
        if self._authorization is None:
            self._authorization = self._authenticator.authenticate()

    def _reauthenticate(self):
        self._authorization = None
        self._check_authorization()

    def _get_authorization_header(
        self, headers: Optional[Dict[str, str]]
    ) -> Mapping[str, str]:
        if self._authorization is None:
            raise HTTPClientException("_authorization cannot be None")

        authorization = self._authorization.copy()

        if headers is None:
            new_headers = authorization
        else:
            new_headers = headers.copy()
            new_headers.update(authorization)

        return new_headers

    def _call_super_request(
        self, method: str, path: str, headers: Optional[Dict[str, str]], **kwargs: Any
    ) -> requests.Response:
        request_headers = self._get_authorization_header(headers)
        return super()._request(method, path, headers=request_headers, **kwargs)

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        self._check_authorization()

        headers = kwargs.pop(self._ARG_HEADERS, None)

        response = self._call_super_request(method, path, headers=headers, **kwargs)

        status_code = response.status_code
        if status_code == 401 or status_code == 403:
            self.log.info("Unauthenticated, trying to reauthenticate...")

            self._reauthenticate()

            response = self._call_super_request(method, path, headers=headers, **kwargs)

        return response
