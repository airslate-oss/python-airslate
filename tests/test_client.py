# This file is part of the airslate.
#
# Copyright (c) 2021-2023 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import responses
from responses import POST

from airslate.client import Client
from airslate.utils import default_headers


@responses.activate
def test_default_headers(client):
    client.headers['key'] = 'value'
    url = f'{client.base_url}/v1/organizations'

    responses.add(POST, url, status=200, body='{}')

    client.post('/v1/organizations', {})
    headers = responses.calls[0].request.headers

    assert headers['key'] == 'value'
    assert headers['User-Agent'] == default_headers()['user-agent']
    assert headers['Accept'] == 'application/json'
    assert headers['Content-Type'] == 'application/json; charset=utf-8'


@responses.activate
def test_request_headers(client):
    url = f'{client.base_url}/v1/organizations'
    responses.add(POST, url, status=200, body='{}')

    client.post('/v1/organizations', {}, headers={
        'User-Agent': 'Test',
        'Content-Type': 'text/plain;charset=UTF-8'
    })

    headers = responses.calls[0].request.headers

    assert headers['User-Agent'] == 'Test'
    assert headers['Content-Type'] == 'text/plain;charset=UTF-8'


@responses.activate
def test_overriding_headers(client):
    client.headers['key1'] = 'value1'
    client.headers['key2'] = 'value2'

    url = f'{client.base_url}/v1/organizations'
    responses.add(POST, url, status=200, body='{}')

    client.post('/v1/organizations', {}, headers={'key1': 'value3'})
    headers = responses.calls[0].request.headers

    assert headers['key1'] == 'value3'
    assert headers['key2'] == 'value2'


@responses.activate
def test_auth_header():
    client = Client(token='secret')

    assert client.headers['Authorization'] == 'Bearer secret'


@responses.activate
def test_collection_response(client):
    url = f'{client.base_url}/v1/organizations'
    response_data = {
        'data': {},
        'meta': {},
    }

    responses.add(POST, url, status=200, json=response_data)
    response = client.post('/v1/organizations', {})

    assert response.json() == response_data


def test_custom_options():
    client = Client()
    assert client.options == {
        'base_url': 'https://api.airslate.io',
        'max_retries': 3,
        'timeout': 5.0,
        'version': 'v1'
    }

    client = Client(foo='1', bar='2', baz='3')
    assert client.options == {
        'bar': '2',
        'base_url': 'https://api.airslate.io',
        'baz': '3',
        'foo': '1',
        'max_retries': 3,
        'timeout': 5.0,
        'version': 'v1'
    }
