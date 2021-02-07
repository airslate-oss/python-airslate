# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Provides document fields related classes and functionality."""


from .base import BaseEntity


class Field(BaseEntity):
    """Represents document fields entity."""

    @property
    def type(self):
        return 'dictionary'
