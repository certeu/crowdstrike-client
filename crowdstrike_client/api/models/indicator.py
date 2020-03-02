# -*- coding: utf-8 -*-
"""CrowdStrike API indicator model module."""

from datetime import datetime
from typing import List, Optional

from crowdstrike_client.api.models.base import Base


class Label(Base):
    """CrowdStrike API label model."""

    name: str
    created_on: datetime
    last_valid_on: datetime


class Relation(Base):
    """CrowdStrike API relation model."""

    id: Optional[str] = None
    indicator: str
    type: str
    created_date: datetime
    last_valid_date: datetime


class Indicator(Base):
    """CrowdStrike API indicator model."""

    _marker: str
    id: str
    type: str
    actors: List[str]
    deleted: bool
    domain_types: List[str]
    indicator: str
    ip_address_types: List[str]
    kill_chains: List[str]
    labels: List[Label]
    last_updated: datetime
    malicious_confidence: str
    malware_families: List[str]
    published_date: datetime
    relations: List[Relation]
    reports: List[str]
    targets: List[str]
    threat_types: List[str]
    vulnerabilities: List[str]
