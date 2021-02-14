# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from airslate.entities.tags import Tag


def test_simple_construct():
    tag = Tag('123')

    assert tag.id == '123'
    assert tag.type == 'flow_tags'
    assert tag.relationships == {}
    assert tag.included == []
    assert tag.meta == {}
    assert tag.object_meta == {}
    assert tag.__repr__() == '<Tag: id=123, type=flow_tags>'
