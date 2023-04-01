# This file is part of the airslate.
#
# Copyright (c) 2021-2023 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

from datetime import datetime

import pytest

from airslate.models import (
    Organization,
    OrganizationSettings,
    OrganizationSettingsContent,
)


@pytest.mark.parametrize(
    'model_cls, kwargs, expected_repr',
    [
        (Organization,
         {'id': 'org1',
          'name': 'Test Org',
          'subdomain': 'test',
          'status': 'active',
          'created_at': datetime(2021, 1, 1),
          'updated_at': datetime(2021, 1, 1),
          'category': None, 'size': None},
         '<Organization: id=org1>'),
        (OrganizationSettings,
         {'id': 'org_settings1', 'settings': {'key': 'value'}},
         '<OrganizationSettings: id=org_settings1>'),
        (OrganizationSettingsContent,
         {'allow_recipient_registration': True,
          'attach_completion_certificate': False,
          'require_electronic_signature_consent': True,
          'allow_reusable_flow': False,
          'verified_domains': ['example.com']},
         '<OrganizationSettingsContent: allow_recipient_registration: True, '
         'attach_completion_certificate: False, '
         'require_electronic_signature_consent: True, '
         'allow_reusable_flow: False, verified_domains: [\'example.com\']>'),
    ]
)
def test_model_creation(model_cls, kwargs, expected_repr):
    model_instance = model_cls(**kwargs)
    assert model_instance.to_dict() == kwargs
    assert repr(model_instance) == expected_repr
