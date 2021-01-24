# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Standard exception hierarchy for airslate.

Classes:

    Error
    BadRequest
    Unauthorized
    RetryError
    RateLimitError

"""


class Error(Exception):
    """Base class for errors in airslate package."""

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


class BadRequest(Error):
    """Error raised for all kinds of bad requests.

    Raise if the client sends something to the server cannot handle.
    """

    def __init__(self, response=None):
        super().__init__(
            message='Bad Request',
            status=400,
            response=response
        )


class Unauthorized(Error):
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


class RetryError(Error):
    """Base class for retryable errors."""

    def __init__(self, message=None, status=None, response=None):
        self.retry_after = None
        super().__init__(
            message=message,
            status=status,
            response=response,
        )


class RateLimitError(RetryError):
    """Error raised for exceeding rate limit.

    The server is limiting the rate at which this client receives responses,
    and this request exceeds that rate.
    """

    def __init__(self, response=None):
        message = ("Exceeded airSlate's Rate Limit. "
                   "Please use time.sleep() to space requests.")

        super().__init__(
            message=message,
            status=429,
            response=response,
        )

        if response is not None:
            self.retry_after = float(response.headers['Retry-After'])


class InternalServerError(RetryError):
    """Internal server error class.

    The server has encountered a situation it doesn't know how to handle.
    """

    def __init__(self, response=None):
        status = 500
        if response:
            status = response.status

        super().__init__(
            message='Internal Server Error',
            status=status,
            response=response,
        )
