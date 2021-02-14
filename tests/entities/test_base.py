# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import pickle

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


def test_set_state():
    state = {
        'data': {
            'attributes': {'name': 'foo'},
            'relationships': {'slate_addon': {}},
            'type': 'dictionary',
            'id': 117,
            'meta': {'a': 'b'},
        },
        'meta': {'c': 'f'},
        'included': [
            {'x': 'y'}
        ]
    }

    entity = MyEntity(8)
    entity.__setstate__(state)

    assert entity.attributes == {'id': 117, 'name': 'foo'}
    assert entity.relationships == {'slate_addon': {}}
    assert entity.type == 'dictionary'
    assert entity.id == 117
    assert entity.object_meta == {'a': 'b'}
    assert entity.meta == {'c': 'f'}
    assert entity.included == [{'x': 'y'}]


def test_get_state():
    entity = MyEntity(42)
    entity.attributes.update({'abc': 'def'})

    serialized = pickle.dumps(entity)
    deserialized = pickle.loads(serialized)

    assert deserialized.id == 42
    assert deserialized.abc == 'def'


def test_get_invalid_attr():
    entity = MyEntity(1)
    with pytest.raises(AttributeError) as exc_info:
        entity.abc

    assert "'MyEntity' object has no attribute 'abc'" in str(exc_info.value)


def test_get_set_attr():
    entity = MyEntity(1)

    assert entity.id == 1
    assert entity['id'] == 1

    assert 'abc' not in entity
    entity.abc = 42

    assert entity.abc == 42
    assert entity['abc'] == 42
    assert 'abc' in entity
