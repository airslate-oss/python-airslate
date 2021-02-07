# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.


import responses
from responses import GET

from airslate.entities.addons import SlateAddonFile


@responses.activate
def test_empty_response(client):
    file_id = '1'
    json = {
        'data': {
            'type': 'slate_addon_files',
            'id': 'D77F5000-0000-0000-0000AE67',
            'relationships': {
                'slate_addon': {}
            },
        }
    }

    responses.add(
        GET,
        f'{client.base_url}/v1/slate-addon-files/{file_id}',
        status=200,
        json=json
    )

    resp = client.slate_addon_files.get(file_id)
    assert isinstance(resp, SlateAddonFile)
