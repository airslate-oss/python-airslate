# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The top-level module for airslate resources.

This module provides base resource class used by various resource
classes within airslate package.

Classes:

    BaseResource

"""

from abc import ABCMeta


# pylint: disable=too-few-public-methods
class BaseResource(metaclass=ABCMeta):
    """Base resource class."""

    API_VERSION = 'v1'

    def __init__(self, client, api_version=None):
        """A :class:`BaseResource` base object for airslate resources."""
        self.client = client
        self.api_version = api_version or BaseResource.API_VERSION

    def resolve_endpoint(self, path: str) -> str:
        """Resolve resource endpoint taking into account API version.

        >>> self.resolve_endpoint('/addon-token')
        /v1/addon-token
        >>> self.resolve_endpoint('addons/slates/0/documents')
        /v1/addons/slates/0/documents
        """
        return f"/{self.api_version}/{path.lstrip('/')}"
