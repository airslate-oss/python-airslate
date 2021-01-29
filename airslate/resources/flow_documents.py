# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Addon flow documents module for airslate package."""

from airslate import resolve_endpoint


class FlowDocuments:  # pylint: disable=too-few-public-methods
    """Addon flow documents resource."""

    def __init__(self, client):
        self.client = client

    def collection(self, flow_id, **options):
        """Get supported documents for given flow."""
        url = resolve_endpoint(
            f'addons/slates/{flow_id}/documents'
        )

        options['query'] = options.pop('query', {})
        return self.client.get(url, **options)
