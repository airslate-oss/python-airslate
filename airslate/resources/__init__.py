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

    def resolve_endpoint(self, path: str) -> str:
        """Resolve resource endpoint taking into account API version.

        >>> resolve_endpoint('/addon-token')
        /v1/addon-token
        >>> resolve_endpoint('addons/slates/0/documents')
        /v1/addons/slates/0/documents
        """
        return '/%s/%s' % (self.API_VERSION, path.lstrip('/'))
