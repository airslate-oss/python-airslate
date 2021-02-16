# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Documents API resource module."""

from airslate.entities.documents import Document
from airslate.entities.fields import Field
from airslate.models.documents import UpdateFields
from . import BaseResource


class Documents(BaseResource):
    """Represent Documents resource."""

    def fields(self, document_id, **options):
        """Get Fields for a given Document."""
        url = self.resolve_endpoint(
            f'documents/{document_id}/fields'
        )

        response = self.client.get(url, full_response=True, **options)
        return Field.from_collection(response)

    def update_fields(self, document_id, fields: UpdateFields):
        """Update Fields for a given Document."""
        url = self.resolve_endpoint(
            f'documents/{document_id}/fields'
        )

        data = fields.to_dict()
        response = self.client.patch(url, full_response=True, data=data)
        return Document.from_one(response)
