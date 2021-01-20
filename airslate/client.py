# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import json
import string
from types import ModuleType

import requests

from . import resources
from .helpers import merge

RESOURCE_CLASSES = {}
for name, module in resources.__dict__.items():
    class_name = string.capwords(name, '_').replace('_', '')
    if class_name == 'BaseResource':
        continue

    if isinstance(module, ModuleType) and class_name in module.__dict__:
        RESOURCE_CLASSES[name] = module.__dict__[class_name]


class Client:
    """airSlate API client class."""

    DEFAULT_CONTENT_TYPE = 'application/vnd.api+json; charset=utf8'

    DEFAULT_OPTIONS = {
        'base_url': 'https://api.airslate.com',
    }

    API_OPTIONS = {}
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

    def __init__(self, session=None, **options):
        """A :class:`Client` object for interacting with airSlate's API."""
        self.session = session or requests.Session()
        self.options = merge(self.DEFAULT_OPTIONS, options)
        self.headers = options.pop('headers', {})

        # Initializes each resource, injecting this client object
        # into the constructor.
        for resource, cls in RESOURCE_CLASSES.items():
            setattr(self, resource, cls(self))

    def request(self, method, path, **options):
        """Dispatches a request to the airSlate API."""
        options = self._merge(options)
        url = options['base_url'] + path
        request_options = self._parse_request_options(options)

        response = getattr(self.session, method)(
            url, **request_options
        )

        return response

    def post(self, path, data, **options):
        """Parses POST request options and dispatches a request."""
        parameter_options = self._parse_parameter_options(options)

        # values in the data body takes precedence
        body = merge(parameter_options, data)

        headers = merge(
            {'Content-Type': self.DEFAULT_CONTENT_TYPE},
            options.pop('headers', {})  # TODO: Add user agent
        )

        return self.request('post', path, data=body, headers=headers, **options)

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
