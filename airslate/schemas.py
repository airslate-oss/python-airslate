# This file is part of the airslate.
#
# Copyright (c) 2021-2023 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Schemas for handling (de)serialized model representation."""

from marshmallow import fields, post_load, RAISE, Schema

from .models import Organization


class OrganizationSchema(Schema):
    """Schema for Organization model."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Metaclass to setup OrganizationSchema."""

        unknown = RAISE
        datetimeformat = '%Y-%m-%dT%H:%M:%S.%f%z'

    id = fields.Str(required=True)
    name = fields.Str(required=True)
    subdomain = fields.Str(required=True)
    category = fields.Str(allow_none=True)
    size = fields.Str(allow_none=True)
    status = fields.Str(required=True)
    created_at = fields.Str(required=True)
    updated_at = fields.Str(required=True)

    @post_load
    def make(self, data, **_kwargs):
        """Deserialize the ``data`` to a Category instance."""
        return Organization(**data)
