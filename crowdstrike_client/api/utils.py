# -*- coding: utf-8 -*-
"""CrowdStrike API utilities module."""

import logging
from logging import Logger
from typing import Any, Mapping

import requests

from crowdstrike_client.api.exceptions import CrowdStrikeException
from crowdstrike_client.api.models.response import ErrorResponse

logger = logging.getLogger(__name__)


def log_error_response(log: Logger, response: requests.Response) -> None:
    status_code = response.status_code

    log.error("Request to '%s' failed with HTTP %d", response.url, status_code)

    error_response = ErrorResponse.parse_http_response(response)
    meta = error_response.meta
    log.error(
        "Failed request meta trace id: %s, query time: %s, powered by: %s",
        meta.trace_id,
        meta.query_time,
        meta.powered_by,
    )

    errors = error_response.errors
    for error in errors:
        log.error("Failed request error: (%s) %s", error.code, error.message)


def remove_mapping_with_none_value(mapping: Mapping[str, Any]) -> Mapping[str, Any]:
    new_mapping = {}
    for k, v in mapping.items():
        if v is not None:
            new_mapping[k] = v
    return new_mapping


def check_response(response: requests.Response, expected_status_code: int) -> None:
    status_code = response.status_code
    if status_code != expected_status_code:
        log_error_response(logger, response)
        raise CrowdStrikeException(f"API call failed with status code {status_code}")


def check_200_response(response: requests.Response) -> None:
    check_response(response, 200)
