# -*- coding: utf-8 -*-
"""CrowdStrike Intel API rules module."""

import logging
from datetime import datetime
from email.utils import format_datetime
from typing import Mapping, Optional

from crowdstrike_client.api.models.download import Download
from crowdstrike_client.api.utils import check_200_response
from crowdstrike_client.http.client import HTTPClient


class Rules:
    """CrowdStrike Intel Rules API."""

    _LATEST_FILES_ENDPOINT = "/intel/entities/rules-latest-files/v1"

    _HEADER_ACCEPT = "Accept"
    _HEADER_IF_NONE_MATCH = "If-None-Match"
    _HEADER_IF_MODIFIED_SINCE = "If-Modified-Since"

    _MIME_APPLICATION_ZIP = "application/zip"

    _PARAM_TYPE = "type"

    def __init__(self, client: HTTPClient) -> None:
        """Initialize CrowdStrike Intel Rules API."""
        self.log = logging.getLogger(__name__)

        self.client = client

    @classmethod
    def _get_request_headers(
        cls, e_tag: Optional[str] = None, last_modified: Optional[datetime] = None
    ) -> Mapping[str, str]:
        headers = {cls._HEADER_ACCEPT: cls._MIME_APPLICATION_ZIP}

        if e_tag is not None:
            headers[cls._HEADER_IF_NONE_MATCH] = f'"{e_tag}"'

        if last_modified is not None:
            headers[cls._HEADER_IF_MODIFIED_SINCE] = format_datetime(
                last_modified, usegmt=True
            )

        return headers

    # TODO: ETag and Last-Modified not working correctly.
    def get_latest_file(
        self,
        rule_set_type: str,
        e_tag: Optional[str] = None,
        last_modified: Optional[datetime] = None,
    ) -> Download:
        """Get the latest rule set as ZIP."""
        path = self._LATEST_FILES_ENDPOINT
        headers = self._get_request_headers(e_tag, last_modified)
        params = {self._PARAM_TYPE: rule_set_type}

        response = self.client.get(path, params=params, headers=headers)
        check_200_response(response)
        return Download.parse_http_response(response)
