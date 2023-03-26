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


@dataclass(frozen=True)
class BaseModel(metaclass=ABCMeta):
    """Base model class."""

    def __getstate__(self):
        """Play nice with pickle."""
        return self.to_dict()

    def to_dict(self):
        """Convert this entity to a dictionary."""
        return {k: str(v) for k, v in asdict(self).items()}


@dataclass(frozen=True)
class Organization(BaseModel):
    """Represent an organization in the airSlate API."""

    id: str  # pylint: disable=invalid-name
    name: str
    subdomain: str
    category: str | None
    size: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    def __repr__(self):
        """Provide an easy-to-read description of the current instance."""
        return f'<Organization: id={self.id}>'