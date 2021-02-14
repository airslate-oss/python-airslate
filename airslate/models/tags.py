# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The base module for Tags request models."""

from asdicts.dict import path

from .base import BaseModel


class Assign(BaseModel):
    """Represents Assign Tags request model."""

    def __init__(self, data=None, included=None, names=None):
        """Initialize Tags model."""
        super().__init__(data, included)
        if names is not None:
            self.data['names'] = names

    def to_dict(self):
        """Convert this model to a dictionary."""
        tags = []

        for name in path(self.data, 'names', []):
            tags.append({
                'type': 'flow_tags',
                'attributes': {
                    'name': name,
                },
            })

        return {'data': tags}
