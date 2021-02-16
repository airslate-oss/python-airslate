# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from airslate.models.documents import UpdateFields
from airslate.entities.fields import Field


def test_empty_update_fields__to_dict():
    model = UpdateFields()
    assert model.to_dict() == {'data': []}


def test_update_fields__to_dict():
    model = UpdateFields(data=[Field('123'), Field('abc')])
    assert model.to_dict() == {'data': [
        {'id': '123', 'type': 'dictionary'},
        {'id': 'abc', 'type': 'dictionary'}
    ]}
