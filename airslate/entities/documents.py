# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from .base import BaseEntity
from .fields import Field


class Document(BaseEntity):
    @property
    def type(self):
        return 'documents'

    @property
    def fields(self):
        return self.has_many(Field, 'fields')
