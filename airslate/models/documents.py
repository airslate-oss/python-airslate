# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The base module for Documents request models."""

from airslate.entities.fields import Field
from .base import BaseModel


class UpdateFields(BaseModel):
    """Represents Update Fields request model."""

    def __init__(self, data: list[Field] = None):
        """Initialize Tags model."""
        super().__init__(data)

    def to_dict(self):
        """Convert this request model to a dictionary."""
        return {'data': [f.to_dict()['data'] for f in self.data]}
