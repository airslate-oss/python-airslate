# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import responses
from responses import GET, PATCH

from airslate.entities.documents import Document
from airslate.entities.documents import Field
from airslate.models.documents import UpdateFields


@responses.activate
def test_empty_fields_response(client):
    document_id = '1'

    responses.add(
        GET,
        f'{client.base_url}/v1/documents/{document_id}/fields',
        status=200,
        json={'data': {}}
    )

    resp = client.documents.fields(document_id)
    headers = responses.calls[0].request.headers

    # There is no 'Content-Type' for GET requests
    assert ('Content-Type' in headers) is False
    assert isinstance(resp, list)


@responses.activate
def test_fields(client):
    document_id = '1'

    responses.add(
        GET,
        f'{client.base_url}/v1/documents/{document_id}/fields',
        status=200,
        json={'data': [
            {
                'type': 'dictionary',
                'id': 'C484F800-0000-0000-000021F6-0001',
                'attributes': {
                    'name': 'heading1.title',
                    'field_type': 'text',
                    'value': 'My Awesome Form',
                    'editors_config_enable': False,
                },
                'relationships': {
                    'editors': {
                        'data': {}
                    }
                }
            }
        ]}
    )

    resp = client.documents.fields(document_id)

    assert isinstance(resp, list)
    assert len(resp) == 1
    assert isinstance(resp[0], Field)


@responses.activate
def test_update_fields(client):
    document_id = '1'

    responses.add(
        PATCH,
        f'{client.base_url}/v1/documents/{document_id}/fields',
        status=200,
        json={'data': {
            'type': 'documents',
            'id': 'C484F800-0000-0000-000021F6',
            'attributes': {
                'name': 'Contact Form',
            }
        }}
    )

    model = UpdateFields(data=[Field('123'), Field('abc')])
    resp = client.documents.update_fields(document_id, model)

    assert isinstance(resp, Document)
    assert resp.id == 'C484F800-0000-0000-000021F6'
    assert resp.name == 'Contact Form'
