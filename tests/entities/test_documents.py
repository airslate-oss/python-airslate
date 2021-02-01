# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import pytest

from airslate.entities.documents import Document, Field
from airslate.exceptions import RelationNotExist


def test_document_assign_includes(documents_collection):
    documents = Document.from_collection(documents_collection)

    assert len(documents) == 1
    assert isinstance(documents[0], Document)
    assert len(documents[0].included) == 2


def test_document_has_many_fields(documents_collection):
    document = Document.from_collection(documents_collection)[0]
    fields = document.fields

    assert isinstance(fields, list)
    assert len(fields) == 2
    assert isinstance(fields[0], Field)
    assert isinstance(fields[1], Field)


def test_document_items(documents_collection):
    document = Document.from_collection(documents_collection)[0]

    assert 'id' in document
    assert 'idx' not in document

    document['idx'] = 42
    assert document['idx'] == 42


def test_document_invalid_has_many(documents_collection):
    document = Document.from_collection(documents_collection)[0]

    with pytest.raises(RelationNotExist) as rel_exc:
        document.has_many(Document, 'foo-bar')

    assert 'No relation with given name' in str(rel_exc.value)


def test_document_has_many_empty_data(documents_collection):
    document = Document.from_collection(documents_collection)[0]

    result = document.has_many(Document, 'pages_file')
    assert isinstance(result, list)
    assert len(result) == 0
