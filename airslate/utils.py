# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Provide utility functions that are used within airslate package."""

from requests.structures import CaseInsensitiveDict

from . import __version__, __url__


def default_user_agent():
    """Return a string representing the default user agent."""
    return f'airslate/{__version__} ({__url__})'


def default_headers():
    """Return a dictionary representing the default request headers."""
    return CaseInsensitiveDict({
        # Default 'User-Agent' header.
        # Usually should be replaced with a more specific value.
        'User-Agent': default_user_agent(),

        # From the JSON:API docs:
        #
        # Clients MUST send all JSON:API data in request documents with
        # the header 'Content-Type: application/vnd.api+json' without any
        # media type parameters.
        'Content-Type': 'application/vnd.api+json',

        # From the JSON:API docs:
        #
        # Servers MUST respond with a '406 Not Acceptable' status code if
        # a request’s 'Accept' header contains the JSON:API media type and
        # all instances of that media type are modified with media type
        # parameters.
        #
        # The client may pass a list of media type parameters to the server.
        # The server finds out that a valid parameter is included.
        'Accept': 'application/vnd.api+json, application/json'
    })
