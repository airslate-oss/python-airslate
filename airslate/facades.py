# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.
#
"""Facades module to provide an easy to access API resources.

Classes:

    Addons
    Flows
    Slates

"""

from .resources import flows, slates, addons


class Addons:
    """Represents Addons API."""

    def __init__(self, client):
        """Initialize Flows instance."""
        self._client = client
        self._files = None
        self._addons = None

    def auth(self, org_id, client_id, client_secret):
        """Get access token for an Addons installed in an Organization."""
        if self._addons is None:
            self._addons = addons.Addons(self._client)
        return self._addons.access_token(org_id, client_id, client_secret)

    @property
    def files(self):
        """Getter for :class:`addons.SlateAddonFiles` instance."""
        if self._files is None:
            self._files = addons.SlateAddonFiles(self._client)
        return self._files


class Flows:  # pylint: disable=too-few-public-methods
    """Represents Flows API."""

    def __init__(self, client):
        """Initialize Flows instance."""
        self._client = client
        self._documents = None

    @property
    def documents(self):
        """Getter for :class:`flows.Documents` instance."""
        if self._documents is None:
            self._documents = flows.Documents(self._client)
        return self._documents


class Slates:  # pylint: disable=too-few-public-methods
    """Represents Slates API."""

    def __init__(self, client):
        """Initialize Slates instance."""
        self._client = client
        self._tags = None

    @property
    def tags(self):
        """Getter for :class:`slates.Tags` instance."""
        if self._tags is None:
            self._tags = slates.Tags(self._client)
        return self._tags
