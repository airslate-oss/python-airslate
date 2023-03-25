# This file is part of the airslate.
#
# Copyright (c) 2021-2023 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Session module for airslate package."""

import warnings

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def create_retry(max_retries=3, backoff_factor=1.0):
    """Create default HTTP adapter based on retry policy."""

    status_forcelist = frozenset({
        408,  # Request Timeout
        429,  # Too Many Requests
        500,  # Internal Server Error
        502,  # Bad Gateway
        503,  # Service Unavailable
        504,  # Gateway Timeout
    })

    method_whitelist = frozenset({
        'DELETE',
        'GET',
        'HEAD',
        'OPTIONS',
        'PUT',
        'POST',
    })

    # Prevent incorrect configuration to avoid hammering API servers
    backoff_factor = abs(float(backoff_factor))
    if backoff_factor == 0.0:
        backoff_factor = 1.0

    max_retries = abs(int(max_retries))

    retry_kwargs = {
        'total': max_retries,
        'read': max_retries,
        'connect': max_retries,
        'backoff_factor': backoff_factor,
        'status_forcelist': status_forcelist
    }

    # urllib3 1.26.0 started issuing a DeprecationWarning for using the
    # 'method_whitelist' init parameter of Retry and announced its removal in
    # version 2.0. The replacement parameter is 'allowed_methods'.
    # Find out which init parameter to use:
    with warnings.catch_warnings():
        warnings.filterwarnings('error')
        try:
            Retry(method_whitelist={})
        except (DeprecationWarning, TypeError):
            retry_methods_param = 'allowed_methods'
        else:
            retry_methods_param = 'method_whitelist'

    retry_kwargs[retry_methods_param] = method_whitelist

    return Retry(**retry_kwargs)


def factory(max_retries=3, backoff_factor=1.0):
    """Create :class:`requests.Session` object.

    Creates a session object that can be used by multiple
    :class:`airslate.client.Client` instances.
    """

    retry_strategy = create_retry(max_retries, backoff_factor)
    adapter = HTTPAdapter(max_retries=retry_strategy)

    session = Session()
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    return session
