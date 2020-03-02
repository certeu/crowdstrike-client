# -*- coding: utf-8 -*-
"""CrowdStrike client module."""

from typing import Optional

from crowdstrike_client.api.authenticator import OAuth2Authenticator
from crowdstrike_client.api.intel import IntelAPI
from crowdstrike_client.http.client import AuthenticatedHTTPClient, HTTPClient


class CrowdStrikeClient:
    """CrowdStrike client."""

    _intel_api: Optional[IntelAPI] = None

    def __init__(self, base_url: str, client_id: str, client_secret: str) -> None:
        """Initialize CrowdStrike client."""
        self.http_client = self._create_http_client(base_url, client_id, client_secret)

    @staticmethod
    def _create_http_client(
        base_url: str, client_id: str, client_secret: str
    ) -> HTTPClient:
        authenticator = OAuth2Authenticator(
            HTTPClient(base_url), client_id, client_secret
        )
        return AuthenticatedHTTPClient(base_url, authenticator)

    @property
    def intel_api(self) -> IntelAPI:
        """CrowdStrike Intel API."""
        if self._intel_api is None:
            self._intel_api = IntelAPI(self.http_client)
        return self._intel_api
