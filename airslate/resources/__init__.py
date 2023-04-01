# This file is part of the airslate.
#
# Copyright (c) 2021-2023 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The top-level module for airslate resources.

This module provides base resource class used by various resource
classes within airslate package.

"""

from abc import ABCMeta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from airslate.client import Client


# pylint: disable=too-few-public-methods
class BaseResource(metaclass=ABCMeta):
    """Base resource class."""

    API_VERSION = 'v1'

    def __init__(self, client: 'Client', api_version=None):
        """A :class:`BaseResource` base object for airslate resources."""
        self.client = client
        self.api_version = api_version or BaseResource.API_VERSION

    def resolve_endpoint(self, path: str) -> str:
        """Resolve resource endpoint taking into account API version.

        >>> from airslate.client import Client
        >>> resource = BaseResource(Client())
        >>> resource.resolve_endpoint('/foo')
        '/v1/foo'
        >>> resource.resolve_endpoint('foo/bar/0/baz')
        '/v1/foo/bar/0/baz'
        """
        return f"/{self.api_version}/{path.lstrip('/')}"
