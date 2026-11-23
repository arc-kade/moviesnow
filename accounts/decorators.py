from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def superuser_required(view_fun):
    @login_required(login_url="accounts:login")
    def wrapper(request,*args,**kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return view_fun(request,*args,**kwargs)
    return wrapper