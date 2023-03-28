# This file is part of the airslate.
#
# Copyright (c) 2021-2023 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import json

import pytest
import responses
from responses import GET

from airslate.exceptions import MissingData
from .factories import OrganizationFactory


@responses.activate
def test_collection(client):
    expected = {
        'meta': {},
        'data': [
            OrganizationFactory(id='5FFE553A-2200-0000-0000D981'),
            OrganizationFactory(id='5FFE553A-2200-0000-0000D982'),
        ],
    }

    url = f'{client.base_url}/v1/organizations'
    responses.add(GET, url, status=200, json=expected)

    organizations = client.organizations.collection()

    actual = json.dumps(
        organizations,
        sort_keys=True,
        default=lambda o: o if isinstance(o, list) else o.to_dict()
    )
    expected = json.dumps(expected['data'], sort_keys=True)
    assert actual == expected


@responses.activate
def test_bad_collection_400(client):
    expected = {'meta': {}}
    url = f'{client.base_url}/v1/organizations'
    responses.add(GET, url, status=200, json=expected)

    with pytest.raises(MissingData) as exc_info:
        _ = client.organizations.collection()

    expected = "API server response is missing the 'data' key"
    assert expected == str(exc_info.value)
