# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

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
    [result.update(obj) for obj in objects]

    return result
