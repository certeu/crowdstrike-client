# -*- coding: utf-8 -*-
"""HTTP authenticator module."""

from abc import ABC, abstractmethod
from typing import Dict


class AuthenticatorException(Exception):
    """Authenticator exception."""

    pass


class AbcAuthenticator(ABC):
    """Abstract authenticator interface."""

    @abstractmethod
    def authenticate(self) -> Dict[str, str]:
        """Perform authentication."""
