from django.conf import settings
from django.shortcuts import redirect

from chessManagement.models import Club


def login_prohibited(view_function):
    def modified_view_function(request,**kwargs):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request,**kwargs)
    return modified_view_function
