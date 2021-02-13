# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from airslate.models.tags import Assign


def test_create_empty_assign_model():
    model = Assign()

    assert model.to_dict() == {'data': []}


def test_names_in_assign_model():
    names = ['foo', 'bar', 'baz']
    model = Assign(names=names)

    assert model.data == {'names': names}

    expected = {'data': [
        {
            'type': 'flow_tags',
            'attributes': {
                'name': 'foo',
            },
        },
        {
            'type': 'flow_tags',
            'attributes': {
                'name': 'bar',
            },
        },
        {
            'type': 'flow_tags',
            'attributes': {
                'name': 'baz',
            },
        }
    ]}
    assert model.to_dict() == expected
