# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Slate addon module for airslate package."""

from airslate.entities.addons import SlateAddonFile
from . import BaseResource


class SlateAddonFiles(BaseResource):
    """Represent slate addon files resource."""

    def get(self, file_id):
        """Get the requested slate addon file."""
        url = self.resolve_endpoint(
            f'slate-addon-files/{file_id}'
        )

        response = self.client.get(url, full_response=True)
        return SlateAddonFile.from_one(response)

    def download(self, file_id):
        """Download contents of the requested file."""
        url = self.resolve_endpoint(
            f'slate-addon-files/{file_id}/download'
        )

        return self.client.get(url, stream=True)
