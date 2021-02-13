# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Provides addons related entities."""

from .base import BaseEntity


class SlateAddon(BaseEntity):
    """Represents Slate Addon entity."""

    @property
    def type(self):
        return 'slate_addons'


class SlateAddonFile(BaseEntity):
    """Represent Slate Addon File entity."""

    @property
    def type(self):
        return 'slate_addon_files'

    @property
    def slate_addon(self) -> SlateAddon:
        """Get :class:`SlateAddon` instance."""
        return self.has_one(SlateAddon, 'slate_addon')
