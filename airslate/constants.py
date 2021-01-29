# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Constants-only module."""

from airslate import __version__, __url__

CONTENT_TYPE_JSON_API = 'application/vnd.api+json'
CONTENT_TYPE_JSON = 'application/json'

# Default 'User-Agent' header. Usually should be replaced
# with a more specific value.
USER_AGENT = f'airslate/{__version__} ({__url__})'

DEFAULT_OPTIONS = {
    # API endpoint base URL to connect to.
    'base_url': 'https://api.airslate.com',

    # The time stop waiting for a response after a given number of seconds.
    # It is not a time limit on the entire response download; rather, an
    # exception is raised if the server has not issued a response for
    # ``timeout`` seconds (more precisely, if no bytes have been received on
    # the underlying socket for ``timeout`` seconds).
    'timeout': 5.0,

    # The number to times to retry if API rate limit is reached or a
    # server error occurs. Rate limit retries delay until the rate limit
    # expires, server errors exponentially backoff starting with a 1 second
    # delay.
    'max_retries': 3,

    # Return the entire JSON response or just ``data`` section.
    'full_response': False,
}

DEFAULT_HEADERS = {
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
QUERY_OPTIONS = {'include'}
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
