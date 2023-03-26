# This file is part of the airslate.
#
# Copyright (c) 2021-2023 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from dataclasses import dataclass
from typing import Optional

from airslate.models import BaseModel


@dataclass(frozen=True)
class FooBar(BaseModel):
    id: str
    name: str
    size: Optional[str] = None


def test_to_dict():
    model = FooBar(id='5FFE553A', name='test')
    expected = {'id': '5FFE553A', 'name': 'test', 'size': None}
    assert model.to_dict() == expected

    model = FooBar(id='5FFE553A', name='test', size='XL')
    expected = {'id': '5FFE553A', 'name': 'test', 'size': 'XL'}
    assert model.to_dict() == expected
