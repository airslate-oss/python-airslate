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
    """Create :class:`requests.Session` object."""
    session = session or Session()
    assert isinstance(session, Session)

    session.headers['User-Agent'] = USER_AGENT
    return session
