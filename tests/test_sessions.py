# This file is part of the airslate.
#
# Copyright (c) 2021-2023 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import pytest
import responses
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError
from responses import POST
from urllib3.util.retry import Retry

from airslate import sessions


def test_retry_default_params():
    retry = sessions.RetryMixin().create_retry()

    assert retry.total == 3
    assert retry.read == 3
    assert retry.connect == 3
    assert retry.redirect == 3
    assert retry.backoff_factor == 1.0
    assert retry.status_forcelist == frozenset({
        408,  # Request Timeout
        429,  # Too Many Requests
        500,  # Internal Server Error
        502,  # Bad Gateway
        503,  # Service Unavailable
        504,  # Gateway Timeout
    })

    retry = sessions.RetryMixin().create_retry(backoff_factor=0)
    assert retry.backoff_factor == 1.0


def test_jwt_default_params(monkeypatch, private_key):
    def get_token(*_args):
        return {'access_token': 'abc', 'expires_in': 123}

    monkeypatch.setattr(sessions.JWTSession, 'get_token', get_token)
    session = sessions.JWTSession(
        client_id='00000000-0000-0000-0000-000000000000',
        user_id='11111111-1111-1111-1111-111111111111',
        key=private_key,
    )

    assert session.client_id == '00000000-0000-0000-0000-000000000000'
    assert session.user_id == '11111111-1111-1111-1111-111111111111'
    assert session.key == private_key
    assert session.auth.token == {'access_token': 'abc', 'expires_in': 123}

    assert len(session.adapters) == 2
    assert isinstance(session.adapters['http://'], HTTPAdapter)
    assert isinstance(session.adapters['https://'], HTTPAdapter)
    assert session.adapters['http://'] == session.adapters['https://']

    adapter = session.adapters['http://']  # type: HTTPAdapter
    assert isinstance(adapter.max_retries, Retry)

    retry = adapter.max_retries  # type: Retry

    assert retry.total == 3
    assert retry.read == 3
    assert retry.connect == 3
    assert retry.redirect == 3
    assert retry.backoff_factor == 1.0
    assert retry.status_forcelist == frozenset({
        408,  # Request Timeout
        429,  # Too Many Requests
        500,  # Internal Server Error
        502,  # Bad Gateway
        503,  # Service Unavailable
        504,  # Gateway Timeout
    })


def test_jwt_update_token(monkeypatch, private_key):
    def get_token(*_args):
        return {'access_token': 'abc', 'expires_in': 123}

    monkeypatch.setattr(sessions.JWTSession, 'get_token', get_token)
    session = sessions.JWTSession(
        client_id='00000000-0000-0000-0000-000000000000',
        user_id='11111111-1111-1111-1111-111111111111',
        key=private_key,
    )

    assert session.auth.token == {'access_token': 'abc', 'expires_in': 123}
    session.update_token({'access_token': 'cde', 'expires_in': 321})
    assert session.auth.token == {'access_token': 'cde', 'expires_in': 321}


@responses.activate
def test_jwt_get_token(private_key):
    responses.add(
        POST,
        'https://oauth.airslate.com/public/oauth/token',
        status=200,
        json={'access_token': 'foobar', 'expires_in': 42},
    )

    session = sessions.JWTSession(
        client_id='00000000-0000-0000-0000-000000000000',
        user_id='11111111-1111-1111-1111-111111111111',
        key=private_key,
    )

    assert session.auth.token == {'access_token': 'foobar', 'expires_in': 42}


@responses.activate
def test_jwt_get_token_bad_request(private_key):
    responses.add(
        POST,
        'https://oauth.airslate.com/public/oauth/token',
        status=400,
        json={
            'error': 'invalid_request',
            'error_description': 'Error description',
            'message': 'Error message',
        }
    )

    with pytest.raises(HTTPError) as exc_info:
        _ = sessions.JWTSession(
            client_id='00000000-0000-0000-0000-000000000000',
            user_id='11111111-1111-1111-1111-111111111111',
            key=private_key,
        )

    assert '400 Client Error: Bad Request for url:' in str(exc_info.value)
