# -*- coding: utf-8 -*-
"""CrowdStrike API download model module."""

import re
from datetime import datetime
from email.utils import parsedate_to_datetime
from io import BytesIO
from typing import Mapping, Optional

import requests

from crowdstrike_client.api.models.base import Base


_HEADER_CONTENT_DISPOSITION = "Content-Disposition"
_HEADER_E_TAG = "ETag"
_HEADER_LAST_MODIFIED = "Last-Modified"

_REGEX_CONTENT_DISPOSITION_FILENAME = re.compile("filename=(.+)")


class Download(Base):
    """CrowdStrike API download model."""

    content: BytesIO
    filename: Optional[str] = None
    e_tag: Optional[str] = None
    last_modified: Optional[datetime] = None

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def parse_http_response(cls, response: requests.Response) -> "Download":
        """Parse HTTP response."""
        content = BytesIO(response.content)

        headers = response.headers
        filename = _extract_filename_from_headers(headers)
        e_tag = _extract_e_tag_from_headers(headers)
        last_modified = _extract_last_modified_from_headers(headers)

        return cls(
            content=content, filename=filename, e_tag=e_tag, last_modified=last_modified
        )


def _extract_filename_from_headers(headers: Mapping[str, str]) -> Optional[str]:
    content_disposition = headers.get(_HEADER_CONTENT_DISPOSITION)
    if content_disposition is None:
        return None

    matches = _REGEX_CONTENT_DISPOSITION_FILENAME.findall(content_disposition)
    if not matches:
        return None

    filename = matches[0].strip('"')
    return filename


def _extract_e_tag_from_headers(headers: Mapping[str, str]) -> Optional[str]:
    e_tag = headers.get(_HEADER_E_TAG)
    if e_tag is None:
        return None

    e_tag = e_tag.strip('"')
    return e_tag


def _extract_last_modified_from_headers(
    headers: Mapping[str, str]
) -> Optional[datetime]:
    last_modified = headers.get(_HEADER_LAST_MODIFIED)
    if last_modified is None:
        return None

    last_modified_datetime = parsedate_to_datetime(last_modified)
    return last_modified_datetime
