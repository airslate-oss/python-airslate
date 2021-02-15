# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from airslate.facades import Flow, Slate
from airslate.resources import flow, slate


def test_getters(client):
    assert isinstance(Flow(client).documents, flow.Documents)
    assert isinstance(Slate(client).tags, slate.Tags)
