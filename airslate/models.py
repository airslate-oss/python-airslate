# This file is part of the airslate.
#
# Copyright (c) 2021-2023 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The top-level module for working with models used by HTTP client.

This module provides classes for representing various data models used by the
HTTP client. These classes can be used for serializing and deserializing data
between the client and server.

Classes:
- Organization: Represents an organization in the airSlate API.

"""

from abc import ABCMeta
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import List, Optional


@dataclass(frozen=True)
class BaseModel(metaclass=ABCMeta):
    """Base model class."""

    def __getstate__(self):
        """Play nice with pickle."""
        return self.to_dict()

    def to_dict(self) -> dict:
        """Convert this entity to a dictionary."""
        return dict(asdict(self).items())


@dataclass(repr=False, frozen=True)
class Organization(BaseModel):  # pylint: disable=too-many-instance-attributes
    """Represent an organization in the airSlate API."""

    id: str  # pylint: disable=invalid-name
    name: str
    subdomain: str
    status: str
    created_at: datetime
    updated_at: datetime
    category: Optional[str] = None
    size: Optional[str] = None

    def __repr__(self):
        """Provide an easy-to-read description of the current instance."""
        return f'<Organization: id={self.id}>'


@dataclass(repr=False, frozen=True)
class OrganizationSettings(BaseModel):
    """Represent an organization settings in the airSlate API."""

    id: str  # pylint: disable=invalid-name
    settings: dict

    def __repr__(self):
        """Provide an easy-to-read description of the current instance."""
        return f'<OrganizationSettings: id={self.id}>'


@dataclass(repr=False, frozen=True)
class OrganizationSettingsContent(BaseModel):
    """Represent an organization settings contents in the airSlate API."""

    allow_recipient_registration: bool
    attach_completion_certificate: bool
    require_electronic_signature_consent: bool
    allow_reusable_flow: bool
    verified_domains: List[str]

    def __repr__(self):
        """Provide an easy-to-read description of the current instance."""
        attrs = [k + ': ' + str(v) for k, v in self.__dict__.items()]
        return f'<OrganizationSettingsContent: {", ".join(attrs)}>'
