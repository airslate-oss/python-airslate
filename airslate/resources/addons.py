# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from .base_resource import BaseResource


class Addons(BaseResource):
    """Addons resource."""

    def __init__(self, client):
        self.client = client

    def access_token(self, org_uid: str, client_id: str, client_secret: str):
        url = self.resolve_endpoint('/addon-token')

        response = self.client.post(url, {
            'client_id': client_id,
            'client_secret': client_secret,
            'organization_id': org_uid,
        })

        return response.json() or {}
