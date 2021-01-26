# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Client module for airslate package."""

import json
import string
import time
from types import ModuleType

import requests

from airslate import exceptions, resources, __version__, __url__
from asdicts.dict import merge


class Client:
    """airSlate API client class."""

    CONTENT_TYPE_JSON_API = 'application/vnd.api+json'
    CONTENT_TYPE_JSON = 'application/json'

    USER_AGENT = f'airslate/{__version__} ({__url__})'

    DEFAULT_OPTIONS = {
        'base_url': 'https://api.airslate.com',
        'timeout': 5.0,
        'max_retries': 3,
    }

    DEFAULT_HEADERS = {
        # Default 'User-Agent' header. Usually should be replaced
        # with a more specific value.
        'User-Agent': USER_AGENT,

        # From the JSON:API docs:
        #
        # Clients MUST send all JSON:API data in request documents with
        # the header 'Content-Type: application/vnd.api+json' without any
        # media type parameters.
        'Content-Type': CONTENT_TYPE_JSON_API,

        # From the JSON:API docs:
        #
        # Servers MUST respond with a '406 Not Acceptable' status code if
        # a request’s 'Accept' header contains the JSON:API media type and
        # all instances of that media type are modified with media type
        # parameters.
        #
        # The client may pass a list of media type parameters to the server.
        # The server finds out that a valid parameter is included.
        'Accept': CONTENT_TYPE_JSON_API + ', ' + CONTENT_TYPE_JSON
    }

    CLIENT_OPTIONS = set(DEFAULT_OPTIONS.keys())
    QUERY_OPTIONS = {'limit', 'offset', 'sync'}
    REQUEST_OPTIONS = {
        'headers',
        'params',
        'data',
        'files',
        'verify',
        'timeout',
    }

    ALL_OPTIONS = (CLIENT_OPTIONS | QUERY_OPTIONS | REQUEST_OPTIONS)

    BACKOFF_FACTOR = 1.0
    RETRY_DELAY = 2.0

    def __init__(self, session=None, **options):
        """A :class:`Client` object for interacting with airSlate's API."""
        self.session = session or requests.Session()
        self.options = merge(self.DEFAULT_OPTIONS, options)
        self.headers = options.pop('headers', {})

        self._init_resources()
        self._init_statuses()

    def request(self, method: str, path: str, **options):
        """Dispatches a request to the airSlate API."""
        options = self._merge(options)
        url = options['base_url'].rstrip('/') + '/' + path.lstrip('/')
        request_options = self._parse_request_options(options)

        retry_count = 0
        while True:
            try:
                response = getattr(self.session, method)(
                    url, **request_options
                )

                if response.status_code in self.statuses:
                    raise self.statuses[response.status_code](
                        response=response
                    )

                # Any unhandled 5xx is a server error
                if 500 <= response.status_code < 600:
                    raise exceptions.InternalServerError(response=response)

                return response
            except exceptions.RetryError as exc:
                if retry_count < options['max_retries']:
                    self._handle_retry_error(exc, retry_count)
                    retry_count += 1
                else:
                    raise exc

    def post(self, path, data, **opts):
        """Parses POST request options and dispatches a request."""
        parameter_options = self._parse_parameter_options(opts)

        # values in the data body takes precedence
        body = merge(parameter_options, data)

        # values in the data opts['headers'] takes precedence
        headers = merge(self.DEFAULT_HEADERS, opts.pop('headers', {}))

        return self.request('post', path, data=body, headers=headers, **opts)

    def _init_resources(self):
        """Initializes each resource and injecting client object into it."""
        resource_classes = {}
        for name, module in resources.__dict__.items():
            cls = string.capwords(name, '_').replace('_', '')
            if isinstance(module, ModuleType) and cls in module.__dict__:
                resource_classes[name] = module.__dict__[cls]

        for name, cls in resource_classes.items():
            setattr(self, name, cls(self))

    def _init_statuses(self):
        """Create a mapping of status codes to classes."""
        self.statuses = {}
        for cls in exceptions.__dict__.values():
            if isinstance(cls, type) and issubclass(cls, exceptions.Error):
                self.statuses[cls().status] = cls

    def _handle_retry_error(self, exc, retry_count):
        """Sleep based on the type of :class:`RetryError`."""
        if isinstance(exc, exceptions.RetryError) and \
                exc.retry_after is not None:
            time.sleep(exc.retry_after)
        else:
            backoff_factor = self.BACKOFF_FACTOR
            retry_delay = self.RETRY_DELAY

            # Prevent incorrect configuration to avoid hammering API servers
            if backoff_factor <= 0.0:
                backoff_factor = 1.0
            if retry_delay <= 0.0:
                retry_delay = 2.0
            time.sleep(backoff_factor * (retry_delay ** retry_count))

    def _parse_parameter_options(self, options):
        """Select all unknown options.

        Select all unknown options (not query string, API, or request
        options)"""
        return self._select_options(options, self.ALL_OPTIONS, invert=True)

    def _parse_request_options(self, options):
        """Select request options out of the provided options object.

        Select and formats options to be passed to the 'requests' library's
        request methods."""
        request_options = self._select_options(options, self.REQUEST_OPTIONS)

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

    def _select_options(self, options, keys, invert=False):
        """Select the provided keys out of an options object.

        Selects the provided keys (or everything except the provided keys) out
        of an options object."""
        options = self._merge(options)
        result = {}

        for key in options:
            if (invert and key not in keys) or (not invert and key in keys):
                result[key] = options[key]

        return result

    def _merge(self, *objects):
        """Merge option objects with the client's object.

        Merges one or more options objects with client's options and returns a
        new options object.
        """
        return merge(self.options, *objects)
