# -*- coding: utf-8 -*-
"""CrowdStrike Intel API indicators module."""

import logging
from typing import Any, List, Mapping, Optional

from crowdstrike_client.api.models import Response
from crowdstrike_client.api.models.indicator import Indicator
from crowdstrike_client.api.utils import (
    check_200_response,
    remove_mapping_with_none_value,
)
from crowdstrike_client.http.client import HTTPClient


class Indicators:
    """CrowdStrike Intel Indicators API."""

    _QUERIES_ENDPOINT = "/intel/queries/indicators/v1"
    _COMBINED_ENDPOINT = "/intel/combined/indicators/v1"
    _ENTITIES_ENDPOINT = "/intel/entities/indicators/GET/v1"

    def __init__(self, client: HTTPClient) -> None:
        """Initialize CrowdStrike Intel Indicators API."""
        self.log = logging.getLogger(__name__)

        self.client = client

    @staticmethod
    def _get_request_params(
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[str] = None,
        fql_filter: Optional[str] = None,
        q: Optional[str] = None,
        include_deleted: Optional[bool] = None,
    ) -> Optional[Mapping[str, Any]]:
        params: Mapping[str, Any] = {
            "offset": offset,
            "limit": limit,
            "sort": sort,
            "filter": fql_filter,
            "q": q,
            "include_deleted": include_deleted,
        }

        params = remove_mapping_with_none_value(params)

        if not params:
            return None

        return params

    def query_ids(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[str] = None,
        fql_filter: Optional[str] = None,
        q: Optional[str] = None,
        include_deleted: Optional[bool] = None,
    ) -> Response[str]:
        """Query list of indicator IDs that match provided FQL filters."""
        path = self._QUERIES_ENDPOINT
        params = self._get_request_params(
            offset, limit, sort, fql_filter, q, include_deleted
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
        include_deleted: Optional[bool] = None,
    ) -> Response[Indicator]:
        """Query list of indicators that match provided FQL filters."""
        path = self._COMBINED_ENDPOINT
        params = self._get_request_params(
            offset, limit, sort, fql_filter, q, include_deleted
        )

        response = self.client.get(path, params=params)
        check_200_response(response)
        return Response.parse_http_response(response, Indicator)

    def get_entities(self, ids: List[str]) -> Response[Indicator]:
        """Get list of specific indicators using their IDs."""
        path = self._ENTITIES_ENDPOINT
        data = {"ids": ids}

        response = self.client.post(path, json=data)
        check_200_response(response)
        return Response.parse_http_response(response, Indicator)
