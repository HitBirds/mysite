from functools import wraps

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url
from django.utils.decorators import available_attrs
from django.utils.six.moves.urllib.parse import urlparse
from django.contrib.auth.decorators import user_passes_test


def staff_required(function=None,redirect_field_name=REDIRECT_FIELD_NAME,login_url=None):
    actual_decorator=user_passes_test(
        lambda u:u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


class Staff_test(object):
    @classmethod
    def as_view(cls,**initkwargs):
        view=super(Staff_test,cls).as_view(**initkwargs)
        return staff_required(view,login_url='www:login')
