# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from airslate.entities.documents import Document, Field


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
