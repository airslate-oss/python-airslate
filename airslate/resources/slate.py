# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Slate API resource module."""

from airslate.entities.tags import Tag
from airslate.models.tags import Assign
from . import BaseResource


class Tags(BaseResource):
    """Represent Tags resource."""

    def collection(self, flow_id, **options):
        """Get tags for a given Flow."""
        url = self.resolve_endpoint(
            f'flows/{flow_id}/packets/tags'
        )

        response = self.client.get(url, full_response=True, **options)
        return Tag.from_collection(response)

    def assign(self, flow_id, packet_id, assign: Assign):
        """Assign tags to a given Flow."""
        url = self.resolve_endpoint(
            f'flows/{flow_id}/packets/{packet_id}/tags'
        )

        data = assign.to_dict()
        response = self.client.post(url, full_response=True, data=data)
        return Tag.from_collection(response)
