# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import responses
from responses import POST

from airslate import constants
from airslate.client import Client


@responses.activate
def test_default_headers(client):
    client.headers['key'] = 'value'
    client.options['full_response'] = True
    url = f'{client.base_url}/v1/addon-token'

    responses.add(POST, url, status=200, body='{}')

    client.post('/v1/addon-token', {})
    headers = responses.calls[0].request.headers

    assert headers['key'] == 'value'
    assert headers['User-Agent'] == constants.USER_AGENT
    assert headers['Content-Type'] == 'application/vnd.api+json'


@responses.activate
def test_request_headers(client):
    url = f'{client.base_url}/v1/addon-token'
    responses.add(POST, url, status=200, body='{}')

    client.options['full_response'] = True
    client.post('/v1/addon-token', {}, headers={
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
    client.options['full_response'] = True

    url = f'{client.base_url}/v1/addon-token'
    responses.add(POST, url, status=200, body='{}')

    client.post('/v1/addon-token', {}, headers={'key1': 'value3'})
    headers = responses.calls[0].request.headers

    assert headers['key1'] == 'value3'
    assert headers['key2'] == 'value2'


@responses.activate
def test_auth_header():
    client = Client(token='secret')

    assert client.headers['Authorization'] == 'Bearer secret'


def test_custom_options():
    client = Client()
    assert client.options == {
        'base_url': 'https://api.airslate.com',
        'max_retries': 3,
        'timeout': 5.0,
        'full_response': False,
    }

    client = Client(foo='1', bar='2', baz='3')
    assert client.options == {
        'bar': '2',
        'base_url': 'https://api.airslate.com',
        'baz': '3',
        'foo': '1',
        'full_response': False,
        'max_retries': 3,
        'timeout': 5.0,
    }
