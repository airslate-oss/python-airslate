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
from airslate.helpers import merge


class Client:
    """airSlate API client class."""

    DEFAULT_CONTENT_TYPE = 'application/vnd.api+json; charset=utf8'
    USER_AGENT = f'airslate/{__version__} ({__url__})'

    DEFAULT_OPTIONS = {
        'base_url': 'https://api.airslate.com',
        'timeout': 5.0,
        'max_retries': 5,
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

    RETRY_DELAY = 1.0
    RETRY_BACKOFF = 2.0

    def __init__(self, session=None, **options):
        """A :class:`Client` object for interacting with airSlate's API."""
        self.session = session or requests.Session()
        self.options = merge(self.DEFAULT_OPTIONS, options)
        self.headers = options.pop('headers', {})

        self._init_resources()
        self._init_statuses()

    def request(self, method, path, **options):
        """Dispatches a request to the airSlate API."""
        options = self._merge(options)
        url = options['base_url'] + path
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

        headers = merge(
            {'Content-Type': self.DEFAULT_CONTENT_TYPE},
            {'User-Agent': self.USER_AGENT},
            opts.pop('headers', {})
        )

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
        """Sleep based on the type of :class:`RetryError`"""
        if isinstance(exc, exceptions.RetryError) and exc.retry_after:
            time.sleep(exc.retry_after)
        else:
            time.sleep(self.RETRY_DELAY * (self.RETRY_BACKOFF ** retry_count))

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
