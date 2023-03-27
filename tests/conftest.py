# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from pathlib import Path

import pytest

from airslate.client import Client


@pytest.fixture
def private_key():
    """Return the private 2048-bit RSA key for testing purposes."""
    return Path(__file__).parent.joinpath('rsa_private.pem').read_bytes()


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
