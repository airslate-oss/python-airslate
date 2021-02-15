# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import json

import responses
from requests import Response
from responses import GET
from responses import POST

from airslate.entities.addons import SlateAddonFile


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

    resp = client.addons.auth(org_id, client_id, client_secret)

    headers = responses.calls[0].request.headers
    body = responses.calls[0].request.body

    assert json.loads(body) == data
    assert headers['Content-Type'] == 'application/json'
    assert isinstance(resp, dict)


@responses.activate
def test_empty_get_response(client):
    file_id = '1'
    json = {
        'data': {
            'type': 'slate_addon_files',
            'id': 'D77F5000-0000-0000-0000AE67',
            'relationships': {
                'slate_addon': {}
            },
        }
    }

    responses.add(
        GET,
        f'{client.base_url}/v1/slate-addon-files/{file_id}',
        status=200,
        json=json
    )

    resp = client.addons.files.get(file_id)
    headers = responses.calls[0].request.headers

    # There is no 'Content-Type' for GET requests
    assert ('Content-Type' in headers) is False
    assert isinstance(resp, SlateAddonFile)


@responses.activate
def test_download(client):
    file_id = '1'

    responses.add(
        GET,
        f'{client.base_url}/v1/slate-addon-files/{file_id}/download',
        status=200,
        stream=True
    )

    resp = client.addons.files.download(file_id)
    headers = responses.calls[0].request.headers

    # There is no 'Content-Type' for GET requests
    assert ('Content-Type' in headers) is False
    assert isinstance(resp, Response)
    assert resp.status_code == 200
