from django.conf import settings
from django.shortcuts import redirect

from chessManagement.models import Club


def login_prohibited(view_function):
    def modified_view_function(request,**kwargs):
        if request.user.is_authenticated:
            return redirect('club_list_home')
        else:
            return view_function(request,**kwargs)
    return modified_view_function
