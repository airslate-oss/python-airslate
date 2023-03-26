# This file is part of the airslate.
#
# Copyright (c) 2021-2023 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Organizations API resource module."""

from typing import List

from airslate.exceptions import MissingData
from airslate.models import Organization
from airslate.schemas import OrganizationSchema
from . import BaseResource


class Organizations(BaseResource):
    """Represent Organizations API resource."""

    def collection(self, **options) -> List[Organization]:
        """Get a list of all Organizations that the current user belongs to."""
        url = self.resolve_endpoint('organizations')
        response = self.client.get(url, **options)

        schema = OrganizationSchema()
        response_data = response.json()
        if 'data' not in response_data:
            raise MissingData()

        return [schema.load(p) for p in response_data['data']]
