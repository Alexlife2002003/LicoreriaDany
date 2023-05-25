from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import render

def group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if not request.user.groups.filter(name=group_name).exists():
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator



class GroupRequiredMixin(AccessMixin):
    group_required = None

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()

        if not self.request.user.groups.filter(name=self.group_required).exists():
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return render(self.request, '403.html', status=403)



