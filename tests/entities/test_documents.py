# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import pytest

from airslate.entities.documents import Document, Field
from airslate.exceptions import RelationNotExist, TypeMismatch


def test_document_assign_includes(documents_collection):
    documents = Document.from_collection(documents_collection)

    assert len(documents) == 1
    assert isinstance(documents[0], Document)
    assert len(documents[0].included) == 2


def test_document_items(documents_collection):
    document = Document.from_collection(documents_collection)[0]

    assert 'id' in document
    assert 'idx' not in document

    document['idx'] = 42
    assert document['idx'] == 42


def test_document_meta(documents_collection):
    document = Document.from_collection(documents_collection)[0]

    assert document.meta['fillable_fields_count'] == 0
    assert document.meta['num_pages'] == 1
    assert document.meta['num_visible_pages'] == 1
    assert 'pdf_file_url' in document.meta


def test_document_included(documents_collection):
    document = Document.from_collection(documents_collection)[0]

    assert isinstance(document.included, list)

    assert len(document.included) == 2
    assert isinstance(document.included[0], dict)
    assert isinstance(document.included[1], dict)


def test_document_invalid_relation(documents_collection):
    document = Document.from_collection(documents_collection)[0]

    with pytest.raises(RelationNotExist) as exc_info:
        document.has_many(Document, 'foo-bar')

    assert 'No relation with given name' in str(exc_info.value)


def test_document_invalid_type():
    api_response = {'data': [
        {'id': 42}
    ]}

    with pytest.raises(TypeMismatch) as exc_info:
        Document.from_collection(api_response)

    assert 'Json type does not match to the entity type' in str(exc_info.value)


def test_document_has_many_empty_data(documents_collection):
    document = Document.from_collection(documents_collection)[0]

    result = document.has_many(Document, 'pages_file')
    assert isinstance(result, list)
    assert len(result) == 0


def test_document_has_many_empty_relations(documents_collection):
    document = Document.from_collection(documents_collection)[0]

    document.relationships['fields']['data'][0]['id'] = 40
    document.relationships['fields']['data'][1]['id'] = 2

    fields = document.has_many(Field, 'fields')

    assert isinstance(fields, list)
    assert len(fields) == 2
    assert isinstance(fields[0], Field)
    assert isinstance(fields[1], Field)
    assert fields[0].id + fields[1].id == 42


def test_document_has_many_fields(documents_collection):
    document = Document.from_collection(documents_collection)[0]
    fields = document.fields

    assert isinstance(fields, list)
    assert len(fields) == 2
    assert isinstance(fields[0], Field)
    assert isinstance(fields[1], Field)
    assert fields[0].id == 'B15E5D00-0000-0000-000021F6-0001'
    assert fields[1].id == 'B15E5D00-0000-0000-000021F6-0002'
