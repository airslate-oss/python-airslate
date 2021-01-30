# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Client module for airslate package."""

import json

from asdicts.dict import merge, intersect_keys
from requests.exceptions import RetryError, RequestException

from . import exceptions, constants, session
from .resources.addons import (
    Addons,
    FlowDocuments
)


class Client:
    """airSlate API client class."""

    def __init__(self, **options):
        """A :class:`Client` object for interacting with airSlate's API."""
        self.options = merge(constants.DEFAULT_OPTIONS, options)
        self.headers = options.pop('headers', {})
        self.session = session.factory(
            max_retries=self.options['max_retries'],
        )

        if 'token' in options:
            self.headers['Authorization'] = f'Bearer {options.pop("token")}'

        self._init_statuses()

        # Initialize each resource and injecting client object into it
        self.addons = Addons(self)
        self.flow_documents = FlowDocuments(self)

    def request(self, method: str, path: str, **options):
        """Dispatches a request to the airSlate API."""
        options = self._merge_options(options)
        url = options['base_url'].rstrip('/') + '/' + path.lstrip('/')
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

            if options['full_response']:
                return response.json()
            return response.json()['data']
        except RetryError as retry_exc:
            raise exceptions.RetryError(
                message='Exceeded API Rate Limit',
                response=retry_exc.response
            )
        except RequestException as req_exc:
            raise exceptions.InternalServerError(
                response=req_exc.response
            )

    def post(self, path, data, **options):
        """Parses POST request options and dispatches a request."""
        parameter_options = self._parse_parameter_options(options)

        # values in the data body takes precedence
        body = merge(parameter_options, data)

        # values in the data options['headers'] takes precedence
        headers = merge(constants.DEFAULT_HEADERS, options.pop('headers', {}))

        return self.request('post', path, data=body, headers=headers,
                            **options)

    def get(self, path, query, **options):
        """Parses GET request options and dispatches a request."""
        query_options = self._parse_query_options(options)
        parameter_options = self._parse_parameter_options(options)

        # query takes precedence
        query = merge(query_options, parameter_options, query)

        # values in the data options['headers'] takes precedence
        headers = merge(constants.DEFAULT_HEADERS, options.pop('headers', {}))

        # `Content-Type` HTTP header should be set only for PUT and POST
        del headers['Content-Type']

        return self.request('get', path, params=query, headers=headers,
                            **options)

    def _init_statuses(self):
        """Create a mapping of status codes to classes."""
        self.statuses = {}
        for cls in exceptions.__dict__.values():
            if isinstance(cls, type) and issubclass(cls, exceptions.Error):
                self.statuses[cls().status] = cls

    def _parse_parameter_options(self, options):
        """Select all unknown options.

        Select all unknown options (not query string, API, or request
        options).
        """
        options = self._merge_options(options)
        return intersect_keys(options, constants.ALL_OPTIONS, invert=True)

    def _parse_query_options(self, options):
        """Select query string options out of the provided options object."""
        options = self._merge_options(options)
        return intersect_keys(options, constants.QUERY_OPTIONS)

    def _parse_request_options(self, options):
        """Select request options out of the provided options object.

        Select and formats options to be passed to the 'requests' library's
        request methods.
        """
        options = self._merge_options(options)
        request_options = intersect_keys(options, constants.REQUEST_OPTIONS)

        if 'params' in request_options:
            params = request_options['params']
            for key in params:
                if isinstance(params[key], bool):
                    params[key] = json.dumps(params[key])

        if 'data' in request_options:
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
