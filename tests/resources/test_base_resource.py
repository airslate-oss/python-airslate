# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import pytest

from airslate.resources import BaseResource


@pytest.mark.parametrize(
    'provided,expected',
    [
        ('addons-token', f'/{BaseResource.API_VERSION}/addons-token'),
        ('/////addons-token', f'/{BaseResource.API_VERSION}/addons-token'),
        ('/addons-token', f'/{BaseResource.API_VERSION}/addons-token'),
    ])
def test_resolve_endpoint(provided, expected):
    resource = BaseResource()
    assert resource.resolve_endpoint(provided) == expected
