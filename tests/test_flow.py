# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from airslate.flow import Flow
from airslate.resources.addons import FlowDocuments
from airslate.resources.flow import Tags


def test_getters(client):
    flow = Flow(client)

    assert isinstance(flow.documents, FlowDocuments)
    assert isinstance(flow.tags, Tags)
