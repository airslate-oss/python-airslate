# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Addons API resource module."""

from airslate.entities.addons import SlateAddonFile
from . import BaseResource


class Addons(BaseResource):
    """Represent Addons API resource."""

    def access_token(self, org_id: str, client_id: str, client_secret: str):
        """Get access token for an Addon installed in an Organization."""
        url = self.resolve_endpoint('addon-token')

        headers = {
            # This is not a JSON:API request
            'Content-Type': 'application/json'
        }

        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'organization_id': org_id,
        }

        return self.client.post(url, data, headers=headers, full_response=True)


class SlateAddonFiles(BaseResource):
    """Represent Slate Addon Files resource."""

    def get(self, file_id):
        """Get the requested Slate Addon File."""
        url = self.resolve_endpoint(
            f'slate-addon-files/{file_id}'
        )

        response = self.client.get(url, full_response=True)
        return SlateAddonFile.from_one(response)

    def download(self, file_id):
        """Download contents of the requested Slate Addon File."""
        url = self.resolve_endpoint(
            f'slate-addon-files/{file_id}/download'
        )

        headers = {'Accept': '*/*'}
        return self.client.get(url, headers=headers, stream=True)
