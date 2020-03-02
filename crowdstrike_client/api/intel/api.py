# -*- coding: utf-8 -*-
"""CrowdStrike Intel API api module."""

import logging
from typing import Optional

from crowdstrike_client.api.intel.actors import Actors
from crowdstrike_client.api.intel.indicators import Indicators
from crowdstrike_client.api.intel.reports import Reports
from crowdstrike_client.api.intel.rules import Rules
from crowdstrike_client.http.client import HTTPClient


class IntelAPI:
    """CrowdStrike Intel API."""

    _actors: Optional[Actors] = None
    _indicators: Optional[Indicators] = None
    _reports: Optional[Reports] = None
    _rules: Optional[Rules] = None

    def __init__(self, client: HTTPClient) -> None:
        """Initialize CrowdStrike Intel API."""
        self.log = logging.getLogger(__name__)

        self.client = client

    @property
    def actors(self) -> Actors:
        """CrowdStrike Intel Actors API."""
        if self._actors is None:
            self._actors = Actors(self.client)
        return self._actors

    @property
    def indicators(self) -> Indicators:
        """CrowdStrike Intel Indicators API."""
        if self._indicators is None:
            self._indicators = Indicators(self.client)
        return self._indicators

    @property
    def reports(self) -> Reports:
        """CrowdStrike Intel Reports API."""
        if self._reports is None:
            self._reports = Reports(self.client)
        return self._reports

    @property
    def rules(self) -> Rules:
        """CrowdStrike Intel Reports API."""
        if self._rules is None:
            self._rules = Rules(self.client)
        return self._rules
