# -*- coding: utf-8 -*-
"""CrowdStrike API actor model module."""

from datetime import datetime
from typing import List, Optional

from crowdstrike_client.api.models.base import Base, Entity, Image


class ECrimeKillChain(Base):
    """CrowdStrike API ECrime kill chain model."""

    attribution: Optional[str] = None
    crimes: Optional[str] = None
    customers: Optional[str] = None
    marketing: Optional[str] = None
    monetization: Optional[str] = None
    rich_text_attribution: Optional[str] = None
    rich_text_crimes: Optional[str] = None
    rich_text_customers: Optional[str] = None
    rich_text_marketing: Optional[str] = None
    rich_text_monetization: Optional[str] = None
    rich_text_services_offered: Optional[str] = None
    rich_text_services_used: Optional[str] = None
    rich_text_technical_tradecraft: Optional[str] = None
    rich_text_victims: Optional[str] = None
    services_offered: Optional[str] = None
    services_used: Optional[str] = None
    technical_tradecraft: Optional[str] = None
    victims: Optional[str] = None


class KillChain(Base):
    """CrowdStrike API kill chain model."""

    actions_and_objectives: Optional[str] = None
    command_and_control: Optional[str] = None
    delivery: Optional[str] = None
    exploitation: Optional[str] = None
    installation: Optional[str] = None
    objectives: Optional[str] = None
    reconnaissance: Optional[str] = None
    rich_text_actions_and_objectives: Optional[str] = None
    rich_text_command_and_control: Optional[str] = None
    rich_text_delivery: Optional[str] = None
    rich_text_exploitation: Optional[str] = None
    rich_text_installation: Optional[str] = None
    rich_text_objectives: Optional[str] = None
    rich_text_reconnaissance: Optional[str] = None
    rich_text_weaponization: Optional[str] = None
    weaponization: Optional[str] = None


class Actor(Base):
    """CrowdStrike API actor model."""

    id: int
    active: bool
    known_as: str
    name: str
    notify_users: bool
    short_description: str
    slug: str
    created_date: Optional[datetime] = None
    last_modified_date: Optional[datetime] = None
    first_activity_date: Optional[datetime] = None
    last_activity_date: Optional[datetime] = None
    motivations: Optional[List[Entity]] = None
    origins: Optional[List[Entity]] = None
    target_countries: Optional[List[Entity]] = None
    target_industries: Optional[List[Entity]] = None
    actor_type: Optional[str] = None
    description: Optional[str] = None
    ecrime_kill_chain: Optional[ECrimeKillChain] = None
    entitlements: Optional[List[Entity]] = None
    group: Optional[Entity] = None
    image: Optional[Image] = None
    kill_chain: Optional[KillChain] = None
    region: Optional[Entity] = None
    rich_text_description: Optional[str] = None
    thumbnail: Optional[Image] = None
    url: Optional[str] = None
