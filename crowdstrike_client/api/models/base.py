# -*- coding: utf-8 -*-
"""CrowdStrike API base model module."""

from typing import Optional

from pydantic import BaseModel


class Base(BaseModel):
    """CrowdStrike API base model."""


class Entity(Base):
    """CrowdStrike API entity model."""

    _id: int
    name: Optional[str] = None
    slug: Optional[str] = None
    value: Optional[str] = None


class Image(Base):
    """CrowdStrike API image model."""

    url: str
    height: Optional[int] = None
    width: Optional[int] = None
