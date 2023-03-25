# This file is part of the airslate.
#
# Copyright (c) 2021-2023 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import pytest
import responses
from responses import POST

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
@pytest.mark.parametrize('status', [505])
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


@responses.activate
@pytest.mark.parametrize('status', [500, 503, 504])
def test_retry_error(status, client):
    responses.add(
        POST,
        f'{client.base_url}/v1/addon-token',
        status=status,
        body='{}',
    )

    with pytest.raises(exceptions.RetryApiError) as exc_info:
        client.post(
            '/v1/addon-token',
            {},
            max_retries=1,
            timeout=0.1,
        )

    assert exc_info.value.status == 503


def test_domain_exception_default_message():
    with pytest.raises(exceptions.DomainError) as exc_info:
        raise exceptions.DomainError()

    assert 'Something went wrong with airSlate API' == str(exc_info.value)


def test_domain_exception_custom_message():
    with pytest.raises(exceptions.DomainError) as exc_info:
        raise exceptions.DomainError('Hello, World!')

    assert 'Hello, World!' == str(exc_info.value)


@responses.activate
def test_notfound(client):
    responses.add(
        POST,
        f'{client.base_url}/v1/a/b/c/d',
        status=404,
        body='{}'
    )

    with pytest.raises(exceptions.NotFoundError):
        client.post('/v1/a/b/c/d', {})
