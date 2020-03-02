# -*- coding: utf-8 -*-
"""CrowdStrike Intel API reports module."""

import logging
from typing import Any, List, Mapping, Optional

from crowdstrike_client.api.exceptions import CrowdStrikeException
from crowdstrike_client.api.models import Response
from crowdstrike_client.api.models.download import Download
from crowdstrike_client.api.models.report import Report
from crowdstrike_client.api.utils import (
    check_200_response,
    log_error_response,
    remove_mapping_with_none_value,
)
from crowdstrike_client.http.client import HTTPClient


class Reports:
    """CrowdStrike Intel Reports API."""

    _QUERIES_ENDPOINT = "/intel/queries/reports/v1"
    _COMBINED_ENDPOINT = "/intel/combined/reports/v1"
    _ENTITIES_ENDPOINT = "/intel/entities/reports/v1"
    _FILES_ENDPOINT = "/intel/entities/report-files/v1"

    _HEADER_ACCEPT = "Accept"

    _MIME_APPLICATION_OCTET_STREAM = "application/octet-stream"

    def __init__(self, client: HTTPClient) -> None:
        """Initialize CrowdStrike Intel Reports API."""
        self.log = logging.getLogger(__name__)

        self.client = client

    @staticmethod
    def _get_request_params(
        report_id: Optional[str] = None,
        ids: Optional[List[str]] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[str] = None,
        fql_filter: Optional[str] = None,
        q: Optional[str] = None,
        fields: Optional[List[str]] = None,
    ) -> Optional[Mapping[str, Any]]:
        params: Mapping[str, Any] = {
            "id": report_id,
            "ids": ids,
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "filter": fql_filter,
            "q": q,
            "fields": fields,
        }

        params = remove_mapping_with_none_value(params)

        if not params:
            return None

        return params

    def query_ids(
        self,
        q: Optional[str] = None,
        fql_filter: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[str] = None,
    ) -> Response[str]:
        """Query list of report IDs that match provided FQL filters."""
        path = self._QUERIES_ENDPOINT
        params = self._get_request_params(
            offset=offset, limit=limit, sort=sort, fql_filter=fql_filter, q=q
        )

        response = self.client.get(path, params=params)
        check_200_response(response)
        return Response.parse_http_response(response, str)

    def query_entities(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[str] = None,
        fql_filter: Optional[str] = None,
        q: Optional[str] = None,
        fields: Optional[List[str]] = None,
    ) -> Response[Report]:
        """Query list of reports that match provided FQL filters."""
        path = self._COMBINED_ENDPOINT
        params = self._get_request_params(
            offset=offset,
            limit=limit,
            sort=sort,
            fql_filter=fql_filter,
            q=q,
            fields=fields,
        )

        response = self.client.get(path, params=params)
        check_200_response(response)
        return Response.parse_http_response(response, Report)

    def get_entities(
        self, ids: List[str], fields: Optional[List[str]] = None
    ) -> Response[Report]:
        """Get list of specific reports using their IDs."""
        path = self._ENTITIES_ENDPOINT
        params = self._get_request_params(ids=ids, fields=fields)

        response = self.client.get(path, params=params)
        check_200_response(response)
        return Response.parse_http_response(response, Report)

    def get_pdf(self, report_id: str) -> Optional[Download]:
        """Get report as PDF."""
        path = self._FILES_ENDPOINT
        headers = {self._HEADER_ACCEPT: self._MIME_APPLICATION_OCTET_STREAM}
        params = self._get_request_params(report_id=report_id)

        response = self.client.get(path, params=params, headers=headers)

        status_code = response.status_code
        if status_code == 200:
            return Download.parse_http_response(response)
        elif status_code == 404:
            self.log.info("No report file for '%s'", report_id)
            return None
        else:
            log_error_response(self.log, response)
            raise CrowdStrikeException(
                f"API call failed with status code {status_code}"
            )
