# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from airslate.facades import Flows, Slates, Addons
from airslate.resources import flows, slates, addons


def test_getters(client):
    assert isinstance(Flows(client).documents, flows.Documents)
    assert isinstance(Slates(client).tags, slates.Tags)
    assert isinstance(Addons(client).files, addons.SlateAddonFiles)
