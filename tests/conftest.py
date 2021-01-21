# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import pytest

from airslate.client import Client


class TestClient(Client):
    def __init__(self):
        super(TestClient, self).__init__(
            base_url='http://airslate.localhost',
        )

    @property
    def base_url(self):
        return self.options['base_url']


@pytest.fixture
def client():
    """Return a test Client instance."""
    return TestClient()
