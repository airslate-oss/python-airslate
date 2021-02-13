# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Provides documents related classes and functionality."""

from .base import BaseEntity
from .fields import Field


class Document(BaseEntity):
    """Represents Document entity."""

    @property
    def type(self):
        return 'documents'

    @property
    def fields(self) -> [Field]:
        """Get list of :class:`Field` instances."""
        return self.has_many(Field, 'fields')
