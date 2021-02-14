# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import pytest

from airslate.entities.addons import SlateAddonFile, SlateAddon
from airslate.exceptions import RelationNotExist, TypeMismatch


def test_from_one(slate_addon_files):
    file = SlateAddonFile.from_one(slate_addon_files)
    addon = file.slate_addon

    assert str(addon) == str(file.has_one(SlateAddon, 'slate_addon'))
    assert file.name == 'example.json'

    assert file.id == slate_addon_files['data']['id']
    assert file.type == 'slate_addon_files'

    assert isinstance(addon, SlateAddon)
    assert addon.type == 'slate_addons'

    relationships = slate_addon_files['data']['relationships']
    assert addon.id == relationships['slate_addon']['data']['id']


def test_has_one_invalid_relation(slate_addon_files):
    file = SlateAddonFile.from_one(slate_addon_files)

    with pytest.raises(RelationNotExist) as exc_info:
        file.has_one(SlateAddon, 'foo-bar')

    assert 'No relation with given name' in str(exc_info.value)


def test_from_one_invalid_type():
    api_response = {'data': [
        {'id': 42}
    ]}

    with pytest.raises(TypeMismatch) as exc_info:
        SlateAddonFile.from_one(api_response)

    assert 'Json type does not match to the entity type' in str(exc_info.value)


def test_has_one_missed_data():
    api_response = {
        'data': {
            'type': 'slate_addon_files',
            'id': 'D77F5000-0000-0000-0000AE67',
            'relationships': {
                'slate_addon': {}
            },
        }
    }

    file = SlateAddonFile.from_one(api_response)
    addon = file.has_one(SlateAddon, 'slate_addon')

    assert addon is None
