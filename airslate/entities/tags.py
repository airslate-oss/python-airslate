# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Provides Tags classes and functionality."""


from .base import BaseEntity


class Tag(BaseEntity):
    """Represents Tags entity."""

    @property
    def type(self):
        return 'flow_tags'
