# This file is part of the airslate.
#
# Copyright (c) 2021-2023 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Session module for airslate package."""

import warnings
from datetime import datetime, timedelta

import jwt
from requests import Session
from requests.adapters import HTTPAdapter
from requests_oauthlib import OAuth2Session
from urllib3.util.retry import Retry


class RetryMixin:  # pylint: disable=too-few-public-methods
    """Implementation of the custom retry policy for HTTP sessions."""

    # Response codes that generally indicate transient network failures
    # and merit client retries,
    STATUSES_WHITELIST = frozenset({
        408,  # Request Timeout
        429,  # Too Many Requests
        500,  # Internal Server Error
        502,  # Bad Gateway
        503,  # Service Unavailable
        504,  # Gateway Timeout
    })

    METHODS_WHITELIST = frozenset({
        'DELETE',
        'GET',
        'HEAD',
        'OPTIONS',
        'PUT',
        'POST',
    })

    def create_retry(self, max_retries=3, backoff_factor=1.0):
        """Create default HTTP adapter based on retry policy."""
        # Prevent incorrect configuration to avoid hammering API servers
        backoff_factor = abs(float(backoff_factor))
        if backoff_factor == 0.0:
            backoff_factor = 1.0

        max_retries = abs(int(max_retries))

        retry_kwargs = {
            'total': max_retries,
            'read': max_retries,
            'connect': max_retries,
            'redirect': max_retries,
            'backoff_factor': backoff_factor,
            'status_forcelist': self.STATUSES_WHITELIST,
        }

        # urllib3 1.26.0 started issuing a DeprecationWarning for using the
        # 'method_whitelist' init parameter of Retry and announced its removal
        # in version 2.0. The replacement parameter is 'allowed_methods'.
        # Find out which init parameter to use:
        with warnings.catch_warnings():
            warnings.filterwarnings('error')
            try:
                Retry(method_whitelist={})
            except (DeprecationWarning, TypeError):
                retry_methods_param = 'allowed_methods'
            else:
                retry_methods_param = 'method_whitelist'

        retry_kwargs[retry_methods_param] = self.METHODS_WHITELIST

        return Retry(**retry_kwargs)


class RetrySession(Session, RetryMixin):
    """Implementation of the :class:`requests.Session` with retry policy.

    The :class:`RetrySession` class inherits from the :class:`requests.Session`
    class and overrides the default behavior of __init__() method to setup a
    predefined retry policy.
    """

    def __init__(self, **kwargs):
        """Initialize a new :class:`RetrySession` object with the specified
        retry policy.

        :keyword int max_retries: The maximum number of times to retry a
            request.
        :keyword float backoff_factor: A multiplier applied to the retry
            interval between attempts.
        """
        super().__init__()

        retry_strategy = self.create_retry(
            kwargs.get('max_retries', 3),
            kwargs.get('backoff_factor', 1.0)
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)

        self.mount('https://', adapter)
        self.mount('http://', adapter)


class JWTSession(Session, RetryMixin):
    """Session class to implement OAuth Grant Type JWT Bearer Flow."""

    token_url = 'https://oauth.airslate.com/public/oauth/token'

    DEFAULT_SCOPE = [
        'openid',
        'email',
        'profile',
        'enterprise',
        'user-client-link',
        'oauth-user-tokens',
    ]

    def __init__(self, client_id: str, user_id: str, key: bytes, **kwargs):
        super().__init__()
        self.client_id = client_id
        self.user_id = user_id
        self.key = key

        scope = kwargs.get('scope', self.DEFAULT_SCOPE)
        self.scope = ' '.join(scope) if isinstance(scope, list) else scope

        self.headers.update(kwargs.get('headers', {}))

        retry_strategy = self.create_retry(
            kwargs.get('max_retries', 3),
            kwargs.get('backoff_factor', 1.0)
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)

        self.mount('https://', adapter)
        self.mount('http://', adapter)

        self.auth = OAuth2Session(
            client_id=self.client_id,
            token=self.get_token(),
            token_updater=self.update_token,
        )

    def update_token(self, token):
        """Update token storage on automatic token refresh.

        This helper function will be used as a call back for
        :class:`requests_oauthlib.OAuth2Session`.
        """
        self.auth.token = token

    def get_token(self):
        """Automatic token retrieve using OAuth Grant Type JWT Bearer Flow."""
        now = datetime.utcnow()

        payload = {
            'aud': self.client_id,
            'sub': self.user_id,
            'iss': 'oauth.airslate.com',
            'iat': now,
            'exp': now + timedelta(minutes=10),
            'scope': self.scope,
        }

        headers = {
            'alg': 'RS256',
            'typ': 'JWT',
        }

        jwt_token = jwt.encode(
            payload=payload,
            key=self.key,
            algorithm='RS256',
            headers=headers,
        )

        response = self.request(
            'POST',
            self.token_url,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={
                'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                'assertion': jwt_token,
            },
        )

        response.raise_for_status()
        return response.json()
