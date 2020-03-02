# -*- coding: utf-8 -*-
"""CrowdStrike Intel API actors module."""

import logging
from typing import Any, List, Mapping, Optional

from crowdstrike_client.api.models import Response
from crowdstrike_client.api.models.actor import Actor
from crowdstrike_client.api.utils import (
    check_200_response,
    remove_mapping_with_none_value,
)
from crowdstrike_client.http.client import HTTPClient


class Actors:
    """CrowdStrike Intel Actors API."""

    _QUERIES_ENDPOINT = "/intel/queries/actors/v1"
    _COMBINED_ENDPOINT = "/intel/combined/actors/v1"
    _ENTITIES_ENDPOINT = "/intel/entities/actors/v1"

    def __init__(self, client: HTTPClient) -> None:
        """Initialize CrowdStrike Intel Actors API."""
        self.log = logging.getLogger(__name__)

        self.client = client

    @staticmethod
    def _get_request_params(
        ids: Optional[List[str]] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[str] = None,
        fql_filter: Optional[str] = None,
        q: Optional[str] = None,
        fields: Optional[List[str]] = None,
    ) -> Optional[Mapping[str, Any]]:
        params: Mapping[str, Any] = {
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
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[str] = None,
        fql_filter: Optional[str] = None,
        q: Optional[str] = None,
    ) -> Response[str]:
        """Query list of actor IDs that match provided FQL filters."""
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
    ) -> Response[Actor]:
        """Query list of actors that match provided FQL filters."""
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
        return Response.parse_http_response(response, Actor)

    def get_entities(
        self, ids: List[str], fields: Optional[List[str]] = None
    ) -> Response[Actor]:
        """Get list of specific actors using their IDs."""
        path = self._ENTITIES_ENDPOINT
        params = self._get_request_params(ids=ids, fields=fields)

        response = self.client.get(path, params=params)
        check_200_response(response)
        return Response.parse_http_response(response, Actor)
