# -*- coding: utf-8 -*-
"""CrowdStrike API report model module."""

from datetime import datetime
from typing import List, Optional

from crowdstrike_client.api.models.base import Base, Entity, Image


class Actor(Base):
    """CrowdStrike API actor model."""

    id: int
    name: Optional[str] = None
    slug: Optional[str] = None
    thumbnail: Optional[Image] = None
    url: Optional[str] = None


class File(Base):
    """CrowdStrike API file model."""

    id: int
    url: str


class Report(Base):
    """CrowdStrike API report model."""

    id: int
    name: str
    slug: str
    actors: List[Actor]
    tags: List[Entity]
    target_countries: List[Entity]
    target_industries: List[Entity]
    motivations: List[Entity]
    created_date: Optional[datetime] = None
    last_modified_date: Optional[datetime] = None
    active: Optional[bool] = None
    attachments: Optional[List[File]] = None
    description: Optional[str] = None
    entitlements: Optional[List[Entity]] = None
    image: Optional[Image] = None
    thumbnail: Optional[Image] = None
    notify_users: Optional[bool] = None
    rich_text_description: Optional[str] = None
    short_description: Optional[str] = None
    topic: Optional[Entity] = None
    type: Optional[Entity] = None
    sub_type: Optional[Entity] = None
    url: Optional[str] = None
