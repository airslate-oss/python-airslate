# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Flows API resource module."""

from airslate.entities.documents import Document
from . import BaseResource


class Documents(BaseResource):
    """Represent Flow Documents API resource."""

    def collection(self, flow_id, **options):
        """Get supported Documents for a given Flow."""
        url = self.resolve_endpoint(
            f'addons/slates/{flow_id}/documents'
        )

        response = self.client.get(url, full_response=True, **options)
        return Document.from_collection(response)
