# This file is part of the airslate.
#
# Copyright (c) 2021-2023 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from dataclasses import dataclass

from airslate.models import BaseModel


@dataclass(frozen=True)
class FooBar(BaseModel):
    id: str
    name: str


def test_to_dict():
    model = FooBar(id='5FFE553A-2200-0000-0000D981', name='test')
    expected = {'id': '5FFE553A-2200-0000-0000D981', 'name': 'test'}

    assert model.to_dict() == expected
