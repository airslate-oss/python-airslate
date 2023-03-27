# This file is part of the airslate.
#
# Copyright (c) 2021-2023 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from airslate import sessions
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


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
