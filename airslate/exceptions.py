# This file is part of the airslate.
#
# Copyright (c) 2021-2023 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Standard exception hierarchy for airslate package."""

from typing import Optional

from requests.models import Response


class BaseError(Exception):
    """Base class for all errors in airslate package."""


class ApiError(BaseError):
    """Base class for errors in API endpoints."""

    def __init__(
            self,
            message: Optional[str] = None,
            status: Optional[int] = None,
            response: Optional[Response] = None
    ):
        errors = []
        reason = None
        request_id = None

        try:
            if response is not None:
                reason = response.reason
                if status is None:
                    status = response.status_code

                json = response.json()

                # The case for:
                #     {
                #         "request_id": "be1ac55e-46b4-4f31-b862-9accac42bba4",
                #         "errors": [
                #             { ...  }
                #         ]
                #     }
                #
                if 'request_id' in json:
                    request_id = json['request_id']

                # The case for:
                #     {
                #         "errors": [
                #             { "message": "..." },
                #             { "message": "..." },
                #             { "message": "..." }
                #         ]
                #     }
                #
                if 'errors' in json:
                    errors = json['errors']

                # The case for:
                #     {
                #         "error": "...",
                #         "error_description": "...",
                #         "hint": "...",
                #         "message": "...",
                #     }
                #
                if 'message' in json:
                    if len(errors) == 0:
                        errors = [{'message': json['message']}]
                    if message is None:
                        message = json['message']
        except ValueError:
            pass

        super().__init__(message or reason)

        # The error message returned by the API.
        self.message = message

        # The reason for the error returned by the API.
        self.reason = reason

        # The HTTP status code returned by the API.
        self.status = status

        # The unique identifier for the API request.
        self.request_id = request_id

        # The original response object returned by the API.
        self.response = response

        # A list of error dictionaries returned by the API.
        self.errors = errors


class BadRequest(ApiError):
    """Error raised for all kinds of bad requests.

    Raise if the client sends something to the server cannot handle.
    """

    def __init__(self, response: Optional[Response] = None):
        super().__init__(
            message='Bad Request',
            status=400,
            response=response
        )


class Unauthorized(ApiError):
    """Error raised for credentials issues on authentication stage.

    It indicates that the request has not been applied because it lacks valid
    authentication credentials for the target resource.
    """

    def __init__(self, response: Optional[Response] = None):
        super().__init__(
            message='Unauthorized',
            status=401,
            response=response
        )


class NotFoundError(ApiError):
    """Error raised when the server can not find the requested resource."""

    def __init__(self, response: Optional[Response] = None):
        super().__init__(
            message='Not Found',
            status=404,
            response=response
        )


class RetryApiError(ApiError):
    """Base class for retryable errors."""

    def __init__(
            self,
            message: Optional[str] = None,
            status: Optional[int] = None,
            response: Optional[Response] = None
    ):
        super().__init__(
            message=message,
            status=status,
            response=response,
        )


class InternalServerError(ApiError):
    """Internal server error class.

    The server has encountered a situation it doesn't know how to handle.
    """

    def __init__(
            self,
            message: Optional[str] = None,
            response: Optional[Response] = None
    ):
        status = 500
        if response is not None:
            status = response.status_code

        if message is None:
            message = 'Internal Server Error'

        super().__init__(
            message=message,
            status=status,
            response=response,
        )


class DomainError(BaseError):
    """Base domain error for airslate package."""

    def __init__(self, message=None):
        if message is None:
            message = 'Something went wrong with airSlate API'

        super().__init__(message)


class MissingData(DomainError):
    """Error raised when ``data`` is missing in JSON:API response."""

    def __init__(self):
        super().__init__('Data is missing in JSON:API response')


class TypeMismatch(DomainError):
    """Error raised when ``data.type`` is invalid."""

    def __init__(self):
        super().__init__('Json type does not match to the entity type')


class RelationNotExist(DomainError):
    """Error raised when there is no relation with given name."""

    def __init__(self):
        super().__init__('No relation with given name')
