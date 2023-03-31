# This file is part of the airslate.
#
# Copyright (c) 2021-2023 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import pytest
import responses
from responses import POST
from typing import Optional
from airslate import exceptions


@pytest.mark.parametrize('message, status, response_data, expected_attrs', [
    (
            None,
            None,
            {'reason': 'Test Reason', 'status_code': 400, 'json': {}},
            {'message': None,
             'reason': 'Test Reason',
             'status': 400,
             'request_id': None,
             'errors': []}
    ),
    (
            'Test Message',
            500,
            {'reason': 'Test Reason',
             'status_code': 500,
             'json': {'message': 'Test JSON Message'}},
            {'message': 'Test Message',
             'reason': 'Test Reason',
             'status': 500,
             'request_id': None,
             'errors': [{'message': 'Test JSON Message'}]}
    ),
    (
            None,
            400,
            {'reason': 'Test Reason',
             'status_code': 400,
             'json': {'request_id': 'test_request_id',
                      'errors': [{'message': 'Error 1'},
                                 {'message': 'Error 2'}]}},
            {'message': None,
             'reason': 'Test Reason',
             'status': 400,
             'request_id': 'test_request_id',
             'errors': [{'message': 'Error 1'},
                        {'message': 'Error 2'}]}
    ),
    (
            None,
            400,
            {'reason': 'Test Reason',
             'status_code': 400,
             'json': {},
             'raise_value_error': True},
            {'message': None,
             'reason': 'Test Reason',
             'status': 400,
             'request_id': None,
             'errors': []}
    ),
    (
            None,
            400,
            {'reason': 'Test Reason',
             'status_code': 400,
             'json': {},
             'raise_value_error': True},
            {'message': None,
             'reason': 'Test Reason',
             'status': 400,
             'request_id': None,
             'errors': []}
    ),
])
def test_api_error_initialization(
        message: Optional[str],
        status: Optional[int],
        response_data: dict,
        expected_attrs: dict,
        mocker
):
    mock_response = mocker.Mock()
    mock_response.reason = response_data['reason']
    mock_response.status_code = response_data['status_code']

    if response_data.get('raise_value_error'):
        mock_response.json.side_effect = ValueError()
    else:
        mock_response.json.return_value = response_data['json']

    error = exceptions.ApiError(
        message=message,
        status=status,
        response=mock_response)

    assert error.message == expected_attrs['message']
    assert error.reason == expected_attrs['reason']
    assert error.status == expected_attrs['status']
    assert error.request_id == expected_attrs['request_id']
    assert error.response == mock_response
    assert error.errors == expected_attrs['errors']


def test_api_error_inheritance():
    assert issubclass(exceptions.ApiError, exceptions.BaseError)


@responses.activate
def test_unauthorized(client):
    responses.add(
        POST,
        f'{client.base_url}/v1/organizations',
        status=401,
        body='{}'
    )

    with pytest.raises(exceptions.Unauthorized):
        client.post('/v1/organizations', {})


@responses.activate
@pytest.mark.parametrize('status', [505])
def test_internal_server_error(status, client):
    responses.add(
        POST,
        f'{client.base_url}/v1/organizations',
        status=status,
        body='{}',
    )

    with pytest.raises(exceptions.InternalServerError) as exc_info:
        client.post(
            '/v1/organizations',
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
        f'{client.base_url}/v1/organizations',
        status=status,
        body='{}',
    )

    with pytest.raises(exceptions.RetryApiError) as exc_info:
        client.post(
            '/v1/organizations',
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
