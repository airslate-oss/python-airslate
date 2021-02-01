# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from airslate.entities.base import filter_included


def test_filter_includes(documents_collection):
    relationships = documents_collection['data'][0]['relationships']
    includes = documents_collection['included']

    result = filter_included(relationships, includes)
    assert len(result) == 2
    assert result[0]['id'] == 'B15E5D00-0000-0000-000021F6-0001'
    assert result[1]['id'] == 'B15E5D00-0000-0000-000021F6-0002'

    result = filter_included({}, includes)
    assert len(result) == 0

    includes[0]['type'] = 'content_file'
    includes[1]['type'] = 'content_file'
    includes[2]['type'] = 'content_file'

    result = filter_included(relationships, includes)
    assert len(result) == 0

    includes[0]['type'] = 'documents'
    includes[0]['id'] = 'BE7F4800-0000-0000-000021F6'

    result = filter_included(relationships, includes)
    assert len(result) == 1
    assert result[0]['type'] == 'documents'
    assert result[0]['id'] == 'BE7F4800-0000-0000-000021F6'
