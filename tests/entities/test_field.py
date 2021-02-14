# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from airslate.entities.documents import Field


def test_simple_construct():
    field = Field('123')

    assert field.id == '123'
    assert field.type == 'dictionary'
    assert field.relationships == {}
    assert field.included == []
    assert field.meta == {}
    assert field.object_meta == {}
    assert field.__repr__() == '<Field: id=123, type=dictionary>'
