# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from airslate.models.base import BaseModel


class FooBar(BaseModel):
    pass


def test_to_dict():
    model = FooBar(
        data={'foo': 'bar'},
        included=[{'foo': {'a': 'b'}}],
    )

    expected = {
        'data': {'foo': 'bar'},
        'included': [{'foo': {'a': 'b'}}]
    }

    assert model.data == {'foo': 'bar'}
    assert model.included == [{'foo': {'a': 'b'}}]
    assert model.to_dict() == expected
