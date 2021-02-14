# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""The base module for airslate models.

This module provides base model class used by various
request models classes within airslate package.

Classes:

    BaseModel

"""

from abc import ABCMeta


class BaseModel(metaclass=ABCMeta):
    """Base model class."""

    def __init__(self, data=None, included=None):
        """Initialize current model."""
        self._data = {} if data is None else data
        self._included = {} if included is None else included

    @property
    def data(self):
        """Getter for data dictionary."""
        return self._data

    @property
    def included(self):
        """Getter for included dictionary."""
        return self._included

    def to_dict(self):
        """Convert this model to a dictionary."""
        payload = {
            'data': self.data
        }

        if len(self.included) > 0:
            payload['included'] = self.included

        return payload
