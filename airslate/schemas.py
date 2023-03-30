# This file is part of the airslate.
#
# Copyright (c) 2021-2023 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Schemas for handling (de)serialized model representation."""

from marshmallow import fields, post_load, EXCLUDE, Schema

from .models import (
    Organization,
    OrganizationSettings,
    OrganizationSettingsContent,
)


class OrganizationSchema(Schema):
    """Schema for :class:`Organization` model."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Metaclass to setup :class:`OrganizationSchema`."""

        unknown = EXCLUDE
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
        """Create a :class:`Organization` instance."""
        return Organization(**data)


class OrganizationSettingContentSchema(Schema):
    """Schema for :class:`OrganizationSettingsContent` model."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Create a :class:`OrganizationSettingContentSchema`."""

        unknown = EXCLUDE

    allow_recipient_registration = fields.Bool(required=True)
    attach_completion_certificate = fields.Bool(required=True)
    require_electronic_signature_consent = fields.Bool(required=True)
    allow_reusable_flow = fields.Bool(required=True)
    verified_domains = fields.List(fields.Str(), required=True)

    @post_load
    def make(self, data, **_kwargs) -> OrganizationSettingsContent:
        """Create a :class:`OrganizationSettingsContent` instance."""
        return OrganizationSettingsContent(**data)


class OrganizationSettingSchema(Schema):
    """Schema for :class:`OrganizationSettings` model."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Metaclass to setup :class:`OrganizationSettingSchema`."""

    unknown = EXCLUDE

    id = fields.Str(required=True)
    settings = fields.Nested(OrganizationSettingContentSchema)

    @post_load
    def make(self, data, **_kwargs) -> OrganizationSettings:
        """Create a :class:`OrganizationSettings` instance."""
        return OrganizationSettings(**data)
