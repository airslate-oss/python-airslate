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
def test_resolve_endpoint(provided, expected, client):
    resource = BaseResource(client)
    assert resource.resolve_endpoint(provided) == expected


@pytest.mark.parametrize(
    'api_version,expected',
    [
        ('v1', '/v1/addons-token'),
        ('v2', '/v2/addons-token'),
        ('v3', '/v3/addons-token'),
        (None, '/v1/addons-token'),
        ('', '/v1/addons-token'),
        (False, '/v1/addons-token'),
    ])
def test_custom_api_version(api_version, expected, client):
    resource = BaseResource(client, api_version)
    assert resource.resolve_endpoint('addons-token') == expected
