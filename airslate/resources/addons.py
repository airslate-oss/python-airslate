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

    def access_token(self, org_id: str, client_id: str, client_secret: str):
        """Get access token for an addon installed in an organization."""
        url = resolve_endpoint('addon-token')

        headers = {
            # This is not JSON:API request
            'Content-Type': self.client.CONTENT_TYPE_JSON
        }

        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'organization_id': org_id,
        }

        response = self.client.post(url, data, headers=headers)

        return response.json() or {}
