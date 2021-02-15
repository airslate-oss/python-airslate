# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import responses
from responses import GET, POST

from airslate.entities.tags import Tag
from airslate.models.tags import Assign


@responses.activate
def test_empty_collection_response(client):
    flow_id = '1'

    responses.add(
        GET,
        f'{client.base_url}/v1/flows/{flow_id}/packets/tags',
        status=200,
        json={'data': {}}
    )

    resp = client.slates.tags.collection(flow_id)
    headers = responses.calls[0].request.headers

    # There is no 'Content-Type' for GET requests
    assert ('Content-Type' in headers) is False
    assert isinstance(resp, list)


@responses.activate
def test_assign(client):
    flow_id = '1'
    packet_id = '2'
    json = {
        'data': [
            {
                'type': 'flow_tags',
                'id': '0A231100-0000-0000-0000943B',
                'attributes': {
                    'name': 'bookkeeping',
                    'created_at': '2021-02-13 14:08:49',
                    'updated_at': '2021-02-14 21:00:01',
                },
            }
        ]
    }

    responses.add(
        POST,
        f'{client.base_url}/v1/flows/{flow_id}/packets/{packet_id}/tags',
        status=200,
        json=json
    )

    tags = Assign(['a_tag'])
    resp = client.slates.tags.assign(flow_id, packet_id, tags)

    assert isinstance(resp, list)
    assert len(resp) == 1
    assert isinstance(resp[0], Tag)
    assert resp[0]['id'] == '0A231100-0000-0000-0000943B'
    assert resp[0]['name'] == 'bookkeeping'
    assert resp[0]['created_at'] == '2021-02-13 14:08:49'
