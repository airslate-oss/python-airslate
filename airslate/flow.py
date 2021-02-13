# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Flow module for airslate package."""

from .resources.addons import FlowDocuments
from .resources.flow import Tags


class Flow:
    """Represents Flow API."""

    def __init__(self, client):
        """Initialize Flow instance."""
        self._client = client
        self._documents = None
        self._tags = None

    @property
    def documents(self):
        """Getter for :class:`FlowDocuments`."""
        if self._documents is None:
            self._documents = FlowDocuments(self._client)
        return self._documents

    @property
    def tags(self):
        """Getter for :class:`Tags`."""
        if self._tags is None:
            self._tags = Tags(self._client)
        return self._tags
