# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Session module for airslate package."""

from requests import Session

from .constants import USER_AGENT


def factory(session=None) -> Session:
    """Create :class:`requests.Session` object.

    Creates a session object that can be used by multiple
    :class:`airslate.client.Client` instances.
    """
    session = session or Session()
    assert isinstance(session, Session)

    # Setting the default 'User-Agent' header. Can be overridden using
    # ``headers`` client option.
    session.headers['User-Agent'] = USER_AGENT

    return session
