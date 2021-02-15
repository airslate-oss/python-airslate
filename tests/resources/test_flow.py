# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import responses
from responses import GET


@responses.activate
def test_empty_collection_response(client):
    flow_id = '1'

    responses.add(
        GET,
        f'{client.base_url}/v1/addons/slates/{flow_id}/documents',
        status=200,
        json={'data': {}}
    )

    resp = client.flows.documents.collection(flow_id, include='fields')
    headers = responses.calls[0].request.headers

    # There is no 'Content-Type' for GET requests
    assert ('Content-Type' in headers) is False
    assert isinstance(resp, list)
