# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Addons module for airslate package."""

from airslate.entities.documents import Document
from . import BaseResource


class Addons(BaseResource):
    """Represent Addons resource."""

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


class FlowDocuments(BaseResource):
    """Represent Flow Documents resource."""

    def collection(self, flow_id, **options):
        """Get supported Documents for a given Flow."""
        url = self.resolve_endpoint(
            f'addons/slates/{flow_id}/documents'
        )

        response = self.client.get(url, full_response=True, **options)
        return Document.from_collection(response)
