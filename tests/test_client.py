# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import responses
from responses import POST


@responses.activate
def test_default_headers(client):
    client.headers['key'] = 'value'
    url = f'{client.base_url}/v1/addon-token'

    responses.add(POST, url, status=200, body='{}')

    client.post('/v1/addon-token', {})
    headers = responses.calls[0].request.headers

    assert headers['key'] == 'value'
    assert headers['User-Agent'] == client.USER_AGENT
    assert headers['Content-Type'] == 'application/vnd.api+json; charset=utf8'


@responses.activate
def test_request_headers(client):
    url = f'{client.base_url}/v1/addon-token'
    responses.add(POST, url, status=200, body='{}')

    client.post('/v1/addon-token', {}, headers={'User-Agent': 'Test'})
    headers = responses.calls[0].request.headers

    assert headers['User-Agent'] == 'Test'
    assert headers['Content-Type'] == 'application/vnd.api+json; charset=utf8'


@responses.activate
def test_overriding_headers(client):
    client.headers['key1'] = 'value1'
    client.headers['key2'] = 'value2'

    url = f'{client.base_url}/v1/addon-token'
    responses.add(POST, url, status=200, body='{}')

    client.post('/v1/addon-token', {}, headers={'key1': 'value3'})
    headers = responses.calls[0].request.headers

    assert headers['key1'] == 'value3'
    assert headers['key2'] == 'value2'