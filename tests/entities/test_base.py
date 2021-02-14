# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import pytest

from airslate.entities.base import filter_included, BaseEntity
from airslate.exceptions import MissingData


class MyEntity(BaseEntity):
    @property
    def type(self):
        return 'dictionary'


def test_filter_includes(documents_collection):
    relationships = documents_collection['data'][0]['relationships']
    includes = documents_collection['included']

    result = filter_included(relationships, includes)
    assert len(result) == 2
    assert result[0]['id'] == 'B15E5D00-0000-0000-000021F6-0001'
    assert result[1]['id'] == 'B15E5D00-0000-0000-000021F6-0002'

    result = filter_included({}, includes)
    assert len(result) == 0

    includes[0]['type'] = 'content_file'
    includes[1]['type'] = 'content_file'
    includes[2]['type'] = 'content_file'

    result = filter_included(relationships, includes)
    assert len(result) == 0

    includes[0]['type'] = 'documents'
    includes[0]['id'] = 'BE7F4800-0000-0000-000021F6'

    result = filter_included(relationships, includes)
    assert len(result) == 1
    assert result[0]['type'] == 'documents'
    assert result[0]['id'] == 'BE7F4800-0000-0000-000021F6'


def test_from_collection():
    with pytest.raises(MissingData) as exc_info:
        BaseEntity.from_collection({})

    assert 'Data is missing in JSON:API response' in str(exc_info.value)


def test_from_one():
    with pytest.raises(MissingData) as exc_info:
        BaseEntity.from_one({})

    assert 'Data is missing in JSON:API response' in str(exc_info.value)


def test_to_dict():
    entity = MyEntity(1)
    assert entity.to_dict() == {'data': {'type': 'dictionary', 'id': 1}}

    entity.attributes.update({'name': 'foo'})
    assert entity.to_dict() == {'data': {
        'attributes': {'name': 'foo'},
        'type': 'dictionary',
        'id': 1,
    }}

    entity.relationships.update({'slate_addon': {}})
    assert entity.to_dict() == {'data': {
        'attributes': {'name': 'foo'},
        'relationships': {'slate_addon': {}},
        'type': 'dictionary',
        'id': 1,
    }}

    entity.object_meta.update({'a': 'b'})
    assert entity.to_dict() == {'data': {
        'attributes': {'name': 'foo'},
        'relationships': {'slate_addon': {}},
        'type': 'dictionary',
        'id': 1,
        'meta': {'a': 'b'},
    }}

    entity.meta.update({'c': 'f'})
    assert entity.to_dict() == {
        'data': {
            'attributes': {'name': 'foo'},
            'relationships': {'slate_addon': {}},
            'type': 'dictionary',
            'id': 1,
            'meta': {'a': 'b'},
        },
        'meta': {'c': 'f'},
    }

    entity.included.append({'x': 'y'})
    assert entity.to_dict() == {
        'data': {
            'attributes': {'name': 'foo'},
            'relationships': {'slate_addon': {}},
            'type': 'dictionary',
            'id': 1,
            'meta': {'a': 'b'},
        },
        'meta': {'c': 'f'},
        'included': [
            {'x': 'y'}
        ]
    }
