# This file is part of the airslate.
#
# Copyright (c) 2021-2023 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Client module for airslate package."""

import json

import requests
from urllib3.exceptions import MaxRetryError
from asdicts.dict import merge, intersect_keys

from . import exceptions, session
from .facades import Flows, Slates, Addons, Documents
from .utils import default_headers


class Client:
    """airSlate API client class."""

    # pylint: disable=too-many-instance-attributes
    # Eight is reasonable in this case.

    DEFAULT_OPTIONS = {
        # API endpoint base URL to connect to.
        'base_url': 'https://api.airslate.com',

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

        # Return the entire JSON response or just ``data`` section. Note, this
        # option should only be modified for direct calls of the client's
        # methods (e.g. ``client.get()``, ``client.post()``, etc). Resource
        # classes can depend on the default value of this option.
        'full_response': False,
    }

    CLIENT_OPTIONS = set(DEFAULT_OPTIONS.keys())

    QUERY_OPTIONS = {
        # Example:
        # '/v1/addons/slates/{flow_id}/documents?include=fields'
        'include',

        # Example:
        # '/v1/{resource}?page=3'
        'page',
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

    def __init__(self, **options):
        """A :class:`Client` object for interacting with airSlate's API."""
        self.options = merge(self.DEFAULT_OPTIONS, options)
        self.headers = options.pop('headers', {})
        self.session = session.factory(
            max_retries=self.options['max_retries'],
        )

        if 'token' in options:
            self.headers['Authorization'] = f'Bearer {options.pop("token")}'

        self._init_statuses()

        # Initialize each resource facade and injecting client object into it
        self.addons = Addons(self)
        self.documents = Documents(self).documents
        self.flows = Flows(self)
        self.slates = Slates(self)

    def request(self, method: str, path: str, **options):
        """Dispatches a request to the airSlate API."""
        options = self._merge_options(options)
        url = options['base_url'].rstrip('/') + '/' + path.lstrip('/')

        # Select and formats options to be passed to the request
        request_options = self._parse_request_options(options)

        try:
            response = getattr(self.session, method)(url, **request_options)

            if response.status_code in self.statuses:
                raise self.statuses[response.status_code](
                    response=response
                )

            # Any unhandled 5xx is a server error
            if 500 <= response.status_code < 600:
                raise exceptions.InternalServerError(response=response)

            if 'stream' in options and options['stream']:
                return response

            response_data = response.json()
            if options['full_response']:
                return response_data

            if 'data' not in response_data:
                raise exceptions.MissingData()

            return response_data['data']
        except (MaxRetryError, requests.exceptions.RetryError) as retry_exc:
            status = None
            response = None

            if hasattr(retry_exc, 'response') and retry_exc.response:
                response = retry_exc.response
            else:
                status = 503

            raise exceptions.RetryApiError(
                message='Exceeded API Rate Limit',
                response=response,
                status=status,
            )
        except requests.exceptions.ConnectionError as conn_exc:
            message = ('A connection attempt failed because the ' +
                       'connected party did not properly respond ' +
                       'after a period of time, or established connection ' +
                       'failed because connected host has failed to respond.')
            raise exceptions.InternalServerError(
                message=message,
                response=conn_exc.response,
            )
        except requests.exceptions.RequestException as req_exc:
            raise exceptions.InternalServerError(
                response=req_exc.response
            )

    def post(self, path, data, **options):
        """Parses POST request options and dispatches a request."""
        return self._create('post', path, data, **options)

    def patch(self, path, data, **options):
        """Parses PATCH request options and dispatches a request."""
        return self._create('patch', path, data, **options)

    def _create(self, method, path, data, **options):
        """Internal helper to send POST/PUT/PATCH requests."""
        # Select all unknown options.
        parameter_options = self._parse_parameter_options(options)

        # Values in the ``data`` takes precedence.
        body = merge(parameter_options, data)

        # Values in the ``options['headers']`` takes precedence.
        headers = merge(default_headers(), options.pop('headers', {}))

        return self.request(method, path, data=body, headers=headers,
                            **options)

    def get(self, path, query=None, **options):
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

    def _parse_query_options(self, options):
        """Select query string options out of the provided options object.

        >>> self._parse_query_options({})
        {}
        >>> self._parse_query_options({'foo': 'bar'})
        {}
        >>> self._parse_query_options({'include': 'fields'})
        {'include': 'fields'}
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
