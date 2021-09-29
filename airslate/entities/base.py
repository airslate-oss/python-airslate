# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The base module for airslate entities.

This module provides base entity class used by various entities
classes within airslate package.

Classes:

    BaseEntity

Functions:

    filter_includes

"""

from abc import ABCMeta, abstractmethod

from asdicts.dict import path

from airslate.exceptions import MissingData, TypeMismatch, RelationNotExist


class BaseEntity(metaclass=ABCMeta):
    """Base entity class."""

    def __init__(self, entity_id):
        """Initialize current entity."""
        self.attributes = {'id': entity_id}
        self.relationships = {}
        self.included = []
        self.meta = {}
        self.object_meta = {}

    def __getattr__(self, item):
        """Invoke for any attr not in the instance's __dict__."""
        if item in super().__getattribute__('attributes'):
            return super().__getattribute__('attributes')[item]

        msg = f"'{self.__class__.__name__}' object has no attribute '{item}'"
        raise AttributeError(msg)

    def __setattr__(self, key, value):
        """Implement setattr(self, name, value)."""
        internal = ['attributes', 'relationships', 'included',
                    'meta', 'object_meta']
        if key in internal:
            return super().__setattr__(key, value)

        return super().__getattribute__('attributes').update({key: value})

    def __getitem__(self, item):
        """Getter for the attribute value."""
        return self.attributes[item]

    def __setitem__(self, key, value):
        """Setter for the attribute value."""
        self.attributes[key] = value

    def __contains__(self, item):
        """Attribute membership verification."""
        return item in self.attributes

    def __repr__(self):
        """Provide an easy to read description of the current entity."""
        return f'<{self.__class__.__name__}: id={self.id}, type={self.type}>'

    def has_one(self, cls, relation_name):
        """Create an instance of the related entity.

        :param cls: The class of the related entity
        :param relation_name: The name of the relation defined in the
            ``relationships`` dictionary
        :return: An instance of the related entity if any or None
        """
        if relation_name not in self.relationships:
            raise RelationNotExist()

        data = path(self.relationships, f'{relation_name}.data')
        if data is None:
            return None

        ids = (path(data, 'id'), path(data, 'type'))
        relations = [e for e in self.included if (e['id'], e['type']) == ids]

        if len(relations) == 0:
            return cls(path(data, 'id'))

        return cls.from_one({'data': relations})

    def has_many(self, cls, relation_name):
        """Create a list of instances of the related entities.

        :param cls: The class of the related entity
        :param relation_name: The name of the relation defined in the
            ``relationships`` dictionary
        :return: A list of instances of the related entities
        """
        if relation_name not in self.relationships:
            raise RelationNotExist()

        data = path(self.relationships, f'{relation_name}.data')
        if data is None:
            return []

        ids = set((r['id'], r['type']) for r in data)
        relations = [e for e in self.included if (e['id'], e['type']) in ids]

        if len(relations) == 0:
            result = map(lambda x: cls(entity_id=x[0]), ids)
            return list(result)

        return cls.from_collection({'data': relations})

    @property
    @abstractmethod
    def type(self):
        """Get type name of the current entity."""

    @classmethod
    def from_one(cls, obj):
        """Create an instance of the current class from the provided data."""
        if 'data' not in obj:
            raise MissingData()

        entity = cls(entity_id=None)
        if path(obj, 'data.type') != entity.type:
            raise TypeMismatch()

        entity.__setstate__({
            'data': {
                'id': path(obj, 'data.id'),
                'attributes': path(obj, 'data.attributes', {}),
                'relationships': path(obj, 'data.relationships', {}),
                'meta': path(obj, 'data.meta', {}),
            },
            'included': filter_included(
                path(obj, 'data.relationships', {}),
                path(obj, 'included', [])
            ),
            'meta': path(obj, 'meta', {}),
        })

        return entity

    @classmethod
    def from_collection(cls, obj):
        """
        Create a list of instances of the current class from the provided data.
        """
        if 'data' not in obj:
            raise MissingData()

        data = obj['data']
        if len(data) == 0:
            return []

        entities = []
        for item in data:
            entity = cls(entity_id=None)

            if path(item, 'type', '') != entity.type:
                raise TypeMismatch()

            entity.__setstate__({
                'data': {
                    'id': path(item, 'id'),
                    'attributes': path(item, 'attributes', {}),
                    'relationships': path(item, 'relationships', {}),
                },
                'included': filter_included(
                    path(item, 'relationships', {}),
                    path(obj, 'included', [])
                ),
                'meta': path(item, 'meta', {}),
            })

            entities.append(entity)

        return entities

    def __getstate__(self):
        """Play nice with pickle."""
        return self.to_dict()

    def __setstate__(self, obj):
        """Play nice with pickle."""
        self.attributes = path(obj, 'data.attributes', {})
        self.attributes['id'] = path(obj, 'data.id')
        self.relationships = path(obj, 'data.relationships', {})
        self.included = path(obj, 'included', [])
        self.meta = path(obj, 'meta', {})
        self.object_meta = path(obj, 'data.meta', {})

    def to_dict(self):
        """Convert this entity to a dictionary."""
        attributes = self.attributes.copy()
        del attributes['id']

        result = {
            'data': {
                'type': self.type,
                'id': self.id,
            }
        }

        if len(attributes) > 0:
            result['data']['attributes'] = attributes

        if len(self.relationships) > 0:
            result['data']['relationships'] = self.relationships

        if len(self.object_meta) > 0:
            result['data']['meta'] = self.object_meta

        if len(self.meta) > 0:
            result['meta'] = self.meta

        if len(self.included) > 0:
            result['included'] = self.included

        return result


def filter_included(relationships, included):
    """Filer a list of ``included`` by nested id from ``relationships``."""
    def normalize(data):
        if data is None:
            return []
        return data if isinstance(data, list) else [data]

    def simplify(relation):
        return ((d['type'], d['id'])
                for i in relation
                for d in normalize(path(relation, f'{i}.data'))
                if 'type' in d)

    r_set = set(simplify(relationships))

    return [e for e in included if (e['type'], e['id']) in r_set]
