# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Standard exception hierarchy for airslate package.

Classes:

    BaseError
    ApiError
    BadRequest
    Unauthorized
    NotFoundError
    RetryError
    InternalServerError
    InvalidTypeError
    DomainError
    MissingData
    TypeMismatch
    RelationNotExist

"""


class BaseError(Exception):
    """Base class for all errors in airslate package."""


class ApiError(BaseError):
    """Base class for errors in API endpoints."""

    def __init__(self, message=None, status=None, response=None):
        super().__init__(message)

        self.status = status
        self.response = response
        self.errors = dict(())

        try:
            if response is not None:
                json = response.json()

                # The case for:
                #     {
                #         "errors": [ { ... }, { ... } ]
                #     }
                #
                if 'errors' in json:
                    self.errors = json['errors']
                    messages = []
                    for error in json['errors']:
                        # The case for:
                        #     {
                        #         "errors": [
                        #             {
                        #                 "title": "",
                        #                 "code": "",
                        #                 "source": "",
                        #             }
                        #         ]
                        #     }
                        #
                        if 'title' in error:
                            messages.append(error['title'])
                        # The case for:
                        #     {
                        #         "errors": [
                        #             {
                        #                 "status": "",
                        #                 "detail": "",
                        #             }
                        #         ]
                        #     }
                        #
                        elif 'detail' in error:
                            messages.append(error['detail'])

                    message = message + ': ' + '; '.join(messages)
                # The case for:
                #     {
                #         "title": "",
                #         "code": "",
                #         "source": "",
                #     }
                #
                elif 'title' in json:
                    self.errors = json
                    message = message + ': ' + json['title']
        except ValueError:
            pass

        self.message = message


class BadRequest(ApiError):
    """Error raised for all kinds of bad requests.

    Raise if the client sends something to the server cannot handle.
    """

    def __init__(self, response=None):
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

    def __init__(self, response=None):
        super().__init__(
            message='Unauthorized',
            status=401,
            response=response
        )


class NotFoundError(ApiError):
    """Error raised when the server can not find the requested resource."""

    def __init__(self, response=None):
        super().__init__(
            message='Not Found',
            status=404,
            response=response
        )


class RetryApiError(ApiError):
    """Base class for retryable errors."""

    def __init__(self, message=None, status=None, response=None):
        super().__init__(
            message=message,
            status=status,
            response=response,
        )


class InternalServerError(ApiError):
    """Internal server error class.

    The server has encountered a situation it doesn't know how to handle.
    """

    def __init__(self, message=None, response=None):
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
