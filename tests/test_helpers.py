# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import pytest

from airslate import API_VERSION
from airslate.helpers import resolve_endpoint


@pytest.mark.parametrize(
    'provided,expected',
    [
        ('addons-token', f'/{API_VERSION}/addons-token'),
        ('/////addons-token', f'/{API_VERSION}/addons-token'),
        ('/addons-token', f'/{API_VERSION}/addons-token'),
    ])
def test_resolve_endpoint(provided, expected):
    assert resolve_endpoint(provided) == expected
