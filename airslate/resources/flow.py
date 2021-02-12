# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Provides flow related classes and functionality."""

from airslate.entities.tags import Tag
from . import BaseResource


class Tags(BaseResource):
    """Represent tags resource."""

    def collection(self, flow_id, **options):
        """Get tags for a given flow."""
        url = self.resolve_endpoint(
            f'flows/{flow_id}/packets/tags'
        )

        response = self.client.get(url, full_response=True, **options)
        return Tag.from_collection(response)
