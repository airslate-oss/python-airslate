# This file is part of the airslate.
#
# Copyright (c) 2021-2023 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Client module for airslate package."""

import json

import requests
from asdicts.dict import merge, intersect_keys
from requests.models import Response
from urllib3.exceptions import MaxRetryError

from . import exceptions, sessions
from .resources.organizations import Organizations
from .utils import default_headers


class Client:
    """airSlate API client class."""

    # pylint: disable=too-many-instance-attributes
    # Eight is reasonable in this case.

    DEFAULT_OPTIONS = {
        # API endpoint base URL to connect to.
        'base_url': 'https://api.airslate.io',

        # The time stop waiting for a response after a given number of seconds.
        # It is not a time limit on the entire response download; rather, an
        # exception is raised if the server has not issued a response for
        # ``timeout`` seconds (more precisely, if no bytes have been received
        # on the underlying socket for ``timeout`` seconds).
        'timeout': 5.0,

        # The number to times to retry if API rate limit is reached or a
        # server error occurs. Rate limit retries delay until the rate limit
        # expires, server errors exponentially backoff starting with a 1 second
        # delay.
        'max_retries': 3,

        # Used API version.
        'version': 'v1',
    }

    CLIENT_OPTIONS = set(DEFAULT_OPTIONS.keys())

    QUERY_OPTIONS = {
        # Page number of the data array you need to view.
        # Example:
        # '/v1/{resource}?page=3'
        'page',

        # Number of elements per page.
        # Example:
        # '/v1/{resource}?per_page=15'
        'per_page',
    }

    REQUEST_OPTIONS = {
        'stream',
        'headers',
        'params',
        'data',
        'files',
        'verify',
        'timeout',
    }

    ALL_OPTIONS = CLIENT_OPTIONS | QUERY_OPTIONS | REQUEST_OPTIONS

    def __init__(self, session=None, auth=None, **options):
        """A :class:`Client` object for interacting with airSlate's API."""
        self.options = merge(self.DEFAULT_OPTIONS, options)
        self.auth = auth

        self.headers = options.pop('headers', {})
        self.session = session or sessions.RetrySession(
            max_retries=self.options['max_retries'],
        )

        self._init_statuses()

        # Initialize each resource facade and injecting client object into it
        self.organizations = Organizations(
            self, api_version=self.options['version'])

    def request(self, method: str, path: str, **options) -> Response:
        """Dispatches a request to the airSlate API."""
        options = self._merge_options(options)
        url = options['base_url'].rstrip('/') + '/' + path.lstrip('/')

        # Select and formats options to be passed to the request
        request_options = self._parse_request_options(options)

        # Select proper session implementation
        current_session = (self.session if self.session.auth is None
                           else self.session.auth)

        try:
            if 'headers' in request_options and request_options['headers']:
                current_session.headers.update(request_options['headers'])
                del request_options['headers']

            # Ensure SSL connection is closed after finished using session.
            with current_session as session:
                response = getattr(session, method)(
                    url, auth=self.auth, **request_options)

            if response.status_code in self.statuses:
                raise self.statuses[response.status_code](
                    response=response
                )

            # Any unhandled 5xx is a server error
            if 500 <= response.status_code < 600:
                raise exceptions.InternalServerError(response=response)

            return response
        except (MaxRetryError, requests.exceptions.RetryError) as retry_exc:
            status = 503
            response = None

            if hasattr(retry_exc, 'response') and retry_exc.response:
                response = retry_exc.response
                status = response.status_code

            raise exceptions.RetryApiError(
                message='Exceeded API Rate Limit',
                response=response,
                status=status,
            )
        except requests.exceptions.ConnectionError as conn_exc:
            message = ('A connection attempt failed because the '
                       'connected party did not properly respond '
                       'after a period of time, or established connection '
                       'failed because connected host has failed to respond.')
            raise exceptions.InternalServerError(
                message=message,
                response=conn_exc.response,
            )
        except requests.exceptions.RequestException as req_exc:
            raise exceptions.InternalServerError(
                response=req_exc.response
            )

    def post(self, path, data, **options) -> Response:
        """Parses POST request options and dispatches a request."""
        return self._create('post', path, data, **options)

    def patch(self, path, data, **options) -> Response:
        """Parses PATCH request options and dispatches a request."""
        return self._create('patch', path, data, **options)

    def _create(self, method, path, data, **options) -> Response:
        """Internal helper to send POST/PUT/PATCH requests."""
        # Select all unknown options.
        parameter_options = self._parse_parameter_options(options)

        # Values in the ``data`` takes precedence.
        body = merge(parameter_options, data)

        # Values in the ``options['headers']`` takes precedence.
        headers = merge(default_headers(), options.pop('headers', {}))

        return self.request(method, path, data=body, headers=headers,
                            **options)

    def get(self, path, query=None, **options) -> Response:
        """Parses GET request options and dispatches a request."""
        # Select query string options.
        query_options = self._parse_query_options(options)

        # Select all unknown options.
        parameter_options = self._parse_parameter_options(options)

        # Values in the ``query`` takes precedence.
        _query = {} if query is None else query
        query = merge(query_options, parameter_options, _query)

        # Values in the ``options['headers']`` takes precedence.
        headers = merge(default_headers(), options.pop('headers', {}))

        # `Content-Type` HTTP header should be set only for PUT and POST
        del headers['Content-Type']

        return self.request('get', path, params=query, headers=headers,
                            **options)

    def _init_statuses(self):
        """Create a mapping of status codes to classes."""
        self.statuses = {}
        for cls in exceptions.__dict__.values():
            if isinstance(cls, type) and issubclass(cls, exceptions.ApiError):
                self.statuses[cls().status] = cls

    def _parse_parameter_options(self, options):
        """Select all unknown options.

        Select all unknown options (not query string, API, or request options).

        >>> self._parse_parameter_options({})
        {}
        >>> self._parse_parameter_options({'foo': 'bar'})
        {'foo': 'bar'}
        >>> self._parse_parameter_options({'timeout': 1.0})
        {}
        """
        options = self._merge_options(options)
        return intersect_keys(options, self.ALL_OPTIONS, invert=True)

    def _parse_query_options(self, options: dict) -> dict:
        """Select query string options out of the provided options object.

        This function selects query string options from the provided `options`
        object based on the pre-defined :attr:`QUERY_OPTIONS` dictionary.
         It returns a new dictionary containing only the key-value pairs that
         match the keys in :attr:`QUERY_OPTIONS`.

        :param options: Dictionary of query string options.
        :type options: dict
        :return: Returns a dictionary of query string options filtered by the
            pre-defined :attr:`QUERY_OPTIONS`.
        :rtype: dict

        Usage:

        >>> self._parse_query_options({})
        {}
        >>> self._parse_query_options({'foo': 'bar'})
        {}
        >>> self._parse_query_options({'per_page': 15})
        {'per_page': 15}
        """
        options = self._merge_options(options)
        return intersect_keys(options, self.QUERY_OPTIONS)

    def _parse_request_options(self, options):
        """Select request options out of the provided options object.

        Select and formats options to be passed to the 'requests' library's
        request methods.

        >>> self._parse_request_options({})
        {'timeout': 5.0, 'headers': {}}
        >>> self._parse_request_options({'timeout': 10.0})
        {'timeout': 10.0, 'headers': {}}
        >>> self._parse_request_options({'params': {'foo': True}})
        {'timeout': 5.0, 'params': {'foo': 'true'}, 'headers': {}}
        >>> self._parse_request_options({'data': {'foo': 'bar'}})
        {'timeout': 5.0, 'data': '{"foo": "bar"}', 'headers': {}}
        >>> self._parse_request_options({'headers': {'x-header': 'value'}})
        {'timeout': 5.0, 'headers': {'x-header': 'value'}}
        """
        options = self._merge_options(options)
        request_options = intersect_keys(options, self.REQUEST_OPTIONS)

        if 'params' in request_options:
            params = request_options['params']
            for key in params:
                # json.dumps(None) -> 'null'
                # json.dumps(True) -> 'true'
                if isinstance(params[key], bool) or params[key] is None:
                    params[key] = json.dumps(params[key])

        if 'data' in request_options:
            # Serialize ``options['data']`` to JSON, requests doesn't do this
            # automatically.
            request_options['data'] = json.dumps(request_options['data'])

        headers = self.headers.copy()
        headers.update(request_options.get('headers', {}))
        request_options['headers'] = headers

        return request_options

    def _merge_options(self, *objects):
        """Merge option objects with the client's object.

        Merges one or more options objects with client's options and returns a
        new options object.
        """
        return merge(self.options, *objects)

    @classmethod
    def jwt_session(cls, client_id, user_id, key, **kwargs):
        """Create an airSlate Client instance with OAuth credentials.

        Constructs an airSlate Client with OAuth Grant Type JWT Bearer Flow
        using ``client_id``, ``user_id`` and ``key``.
        """
        return cls(sessions.JWTSession(client_id, user_id, key, **kwargs))
