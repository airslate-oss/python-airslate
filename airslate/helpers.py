# This file is part of the airslate.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code.

"""Helpers used by various functions within airslate package."""

from . import API_VERSION


def resolve_endpoint(path: str):
    """Resolve resource endpoint taking into account API version."""
    return '/%s/%s' % (API_VERSION, path.lstrip('/'))
