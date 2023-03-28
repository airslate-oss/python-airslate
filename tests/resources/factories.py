# This file is part of the airslate.
#
# Copyright (c) 2021-2023 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

import factory


class OrganizationFactory(factory.DictFactory):
    id = '5FFE553A-2200-0000-0000D981'
    name = 'Acme, Inc.'
    subdomain = 'acme'
    status = 'FINISHED'
    category = 'PROFESSIONAL_AND_BUSINESS'
    size = '0-5'
    created_at = '2022-02-09T09:44:58Z'
    updated_at = '2022-10-28T03:59:10Z'
