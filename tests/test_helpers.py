# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import pytest

from airslate.helpers import merge


@pytest.mark.parametrize(
    'provided,expected',
    [
        ([{'a': 42}, {'foo': 'bar'}], {'a': 42, 'foo': 'bar'}),
        ([{'a': 42}, {'foo': 'bar', 'a': 17}], {'a': 17, 'foo': 'bar'}),
        ([{'a': 17, 'foo': 'bar'}], {'a': 17, 'foo': 'bar'}),
        ([{'a': 1}, {'b': 2}, {'c': 3}, {'a': 4}], {'a': 4, 'b': 2, 'c': 3}),
    ])
def test_merge(provided, expected):
    assert merge(*provided) == expected
