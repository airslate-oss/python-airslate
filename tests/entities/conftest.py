# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import pytest


@pytest.fixture
def documents_collection():
    host = 'http://airslate.localhost'
    original_file_id = '5D645110-0000-0000-000045B9'
    expires = '1539764251'
    signature = 'fd3950b0ea7f954b45df7e3a5fb103b1'

    pdf_file_url = '{}/v1/download/{}?expires={}&signature={}'.format(
        host,
        original_file_id,
        expires,
        signature,
    )

    return {
        'data': [
            {
                'type': 'documents',
                'id': '87915800-0000-0000-000021F6',
                'attributes': {
                    'name': 'fillable.pdf',
                    'status': 'DRAFT',
                    'version': 1,
                    'is_filled': True,
                    'pdf_status': 'COMPLETED',
                    'created_at': '2018-10-17 07:03:44',
                    'updated_at': '2018-10-17 07:03:44'
                },
                'relationships': {
                    'author': {
                        'data': {
                            'type': 'users',
                            'id': '22DB1A00-0000-0000-00009BC6'
                        }
                    },
                    'parent': {
                        'data': {
                            'id': 'BE7F4800-0000-0000-000021F6',
                            'type': 'documents'
                        }
                    },
                    'pages_file': {'data': None},
                    'attributes_file': {'data': None},
                    'content_file': {'data': None},
                    'fields_file': {'data': None},
                    'roles_file': {'data': None},
                    'comments_file': {'data': None},
                    'original_file': {
                        'data': {
                            'type': 'files',
                            'id': original_file_id
                        }
                    },
                    'image_file': {'data': None},
                    'pdf_file': {
                        'data': {
                            'type': 'files',
                            'id': original_file_id
                        }
                    },
                    'fields': {
                        'data': [
                            {
                                'type': 'dictionary',
                                'id': 'B15E5D00-0000-0000-000021F6-0001'
                            },
                            {
                                'type': 'dictionary',
                                'id': 'B15E5D00-0000-0000-000021F6-0002'
                            }
                        ]
                    }
                },
                'meta': {
                    'pdf_file_url': pdf_file_url,
                    'fillable_fields_count': 0,
                    'num_pages': 1,
                    'num_visible_pages': 1,
                }
            }
        ],
        'included': [
            {
                'type': 'dictionary',
                'id': 'B15E5D00-0000-0000-000021F6-0001',
                'attributes': {
                    'name': 'last_name',
                    'field_type': 'text',
                    'value': None,
                    'dropdown_options': None,
                    'radio_buttons_group': None,
                    'required': True,
                }
            },
            {
                'type': 'dictionary',
                'id': 'B15E5D00-0000-0000-000021F6-0002',
                'attributes': {
                    'name': 'amount',
                    'field_type': 'text',
                    'value': None,
                    'dropdown_options': None,
                    'radio_buttons_group': None,
                    'required': True,
                }
            },
            {
                'type': 'dictionary',
                'id': 'B15E5D00-0000-0000-000021F6-0003',
                'attributes': {
                    'name': 'age',
                    'field_type': 'text',
                    'value': None,
                    'dropdown_options': None,
                    'radio_buttons_group': None,
                    'required': False,
                }
            },
        ]
    }


@pytest.fixture
def slate_addon_files():
    host = 'http://airslate.localhost'
    file_id = 'C41CDE20-0000-0000-000045B9'

    return {
        'data': {
            'type': 'slate_addon_files',
            'id': 'D77F5000-0000-0000-0000AE67',
            'attributes': {
                'name': 'example.json',
                'size': 733
            },
            'relationships': {
                'slate_addon': {
                    'data': {
                        'type': 'slate_addons',
                        'id': '09867A00-0000-0000-000093F0'
                    }
                }
            },
            'meta': {
                'download_url': (f'{host}/v1/slate-addon-files/{file_id}' +
                                 '/download')
            }
        }
    }
