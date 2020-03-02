# -*- coding: utf-8 -*-
"""CrowdStrike API response model module."""

import logging
from typing import Any, Generic, List, Optional, Type, TypeVar

import requests

from pydantic import BaseModel, parse_obj_as, validator
from pydantic.generics import GenericModel

from crowdstrike_client.api.models.base import Base

logger = logging.getLogger(__name__)


T = TypeVar("T")


class Pagination(Base):
    """CrowdStrike API pagination model."""

    limit: int
    offset: int
    total: int


class Meta(Base):
    """CrowdStrike API meta model."""

    trace_id: str
    query_time: float
    powered_by: Optional[str] = None
    pagination: Optional[Pagination] = None


class Error(Base):
    """CrowdStrike API error model."""

    id: Optional[str] = None
    code: int
    message: str


class Response(GenericModel, Generic[T]):
    """CrowdStrike API response model."""

    meta: Meta
    errors: List[Error]
    resources: List[T]

    @validator("resources", pre=True)
    def if_resources_none_return_empty_list(cls, resources: Any):
        if resources is None:
            return []
        return resources

    @staticmethod
    def parse_http_response(
        response: requests.Response, resource_type: Type[T]
    ) -> "Response[T]":
        """Parse response object to Response model."""
        # TODO: Is the 'Response[resource_type]' type hint correct?
        return parse_obj_as(Response[resource_type], response.json())  # type: ignore


class ErrorResponse(BaseModel):
    """CrowdStrike API error response model."""

    meta: Meta
    errors: List[Error]

    @classmethod
    def parse_http_response(cls, response: requests.Response) -> "ErrorResponse":
        """Parse response object to ErrorResponse model."""
        return parse_obj_as(cls, response.json())
