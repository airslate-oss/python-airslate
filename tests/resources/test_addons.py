# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import json

import responses
from responses import POST


@responses.activate
def test_access_token(client):
    org_id = '2'
    client_id = '1'
    client_secret = 'secret'

    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'organization_id': org_id,
    }

    responses.add(
        POST,
        f'{client.base_url}/v1/addon-token',
        status=200,
        body=json.dumps(data)
    )

    resp = client.addons.access_token(org_id, client_id, client_secret)

    headers = responses.calls[0].request.headers
    body = responses.calls[0].request.body

    assert json.loads(body) == data
    assert headers['Content-Type'] == 'application/json'
    assert isinstance(resp, dict)
