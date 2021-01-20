# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Helpers used by various functions within airslate package."""

from . import API_VERSION


def merge(*objects):
    """Merge one or more objects into a new object.

    >>> merge({'a': 42}, {'foo': 'bar'})
    {'a': 42, 'foo': 'bar'}
    >>> merge({'a': 42}, {'foo': 'bar', 'a': 17})
    {'a': 17, 'foo': 'bar'}
    >>>  merge({'a': 17, 'foo': 'bar'})
    {'a': 17, 'foo': 'bar'}
    >>> merge({'a': 1}, {'b': 2}, {'c': 3}, {'a': 4})
    {'a': 4, 'b': 2, 'c': 3}
    """
    result = {}
    # pylint: disable=expression-not-assigned
    [result.update(obj) for obj in objects]

    return result


def resolve_endpoint(path: str):
    """Resolve resource endpoint taking into account API version."""
    return '/%s/%s' % (API_VERSION, path.lstrip('/'))
