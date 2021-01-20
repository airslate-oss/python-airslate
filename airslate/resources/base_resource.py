# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

class BaseResource:
    API_VERSION = 'v1'

    @classmethod
    def resolve_endpoint(cls, path: str):
        return '/%s/%s' % (cls.API_VERSION, path.lstrip('/'))
