# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.
#
"""Facades module to provide an easy to access API resources.

Classes:

    Flow
    Slate

"""

from .resources import flow, slate


class Flow:  # pylint: disable=too-few-public-methods
    """Represents Flow API."""

    def __init__(self, client):
        """Initialize Flow instance."""
        self._client = client
        self._documents = None

    @property
    def documents(self):
        """Getter for :class:`flow.Documents` instance."""
        if self._documents is None:
            self._documents = flow.Documents(self._client)
        return self._documents


class Slate:  # pylint: disable=too-few-public-methods
    """Represents Slate API."""

    def __init__(self, client):
        """Initialize Slate instance."""
        self._client = client
        self._tags = None

    @property
    def tags(self):
        """Getter for :class:`slate.Tags` instance."""
        if self._tags is None:
            self._tags = slate.Tags(self._client)
        return self._tags
