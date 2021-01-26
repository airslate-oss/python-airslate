# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Addons module for airslate package."""

from airslate import resolve_endpoint


class Addons:  # pylint: disable=too-few-public-methods
    """Addons resource."""

    def __init__(self, client):
        self.client = client

    def access_token(self, client_id: str, client_secret: str, org_uid: str):
        """Get access token for an addon installed in an organization."""
        url = resolve_endpoint('addon-token')

        response = self.client.post(url, {
            'client_id': client_id,
            'client_secret': client_secret,
            'organization_id': org_uid,
        })

        return response.json() or {}
