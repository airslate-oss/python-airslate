# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import responses
from responses import POST
import pytest
from airslate import exceptions


@responses.activate
def test_unauthorized(client):
    responses.add(
        POST,
        f'{client.base_url}/v1/addon-token',
        status=401,
        body='{}'
    )

    with pytest.raises(exceptions.Unauthorized):
        client.post('/v1/addon-token', {})


@responses.activate
def test_rate_limit(client):
    responses.add(
        POST,
        f'{client.base_url}/v1/addon-token',
        status=429,
        body='{}',
        headers={'Retry-After': '0.42'},
    )

    with pytest.raises(exceptions.RateLimitError) as exc_info:
        client.post(
            '/v1/addon-token',
            {},
            max_retries=1,
            timeout=0.1,
        )

    assert exc_info.value.retry_after == 0.42


@responses.activate
@pytest.mark.parametrize('status', [500, 503, 505])
def test_internal_server_error(status, client):
    responses.add(
        POST,
        f'{client.base_url}/v1/addon-token',
        status=status,
        body='{}',
    )

    with pytest.raises(exceptions.InternalServerError) as exc_info:
        client.post(
            '/v1/addon-token',
            {},
            max_retries=1,
            timeout=0.1,
        )

    assert exc_info.value.status == status
