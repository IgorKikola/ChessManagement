from django.conf import settings
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Club

def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request)
    return modified_view_function

def valid_club_required(view_function):
    def modified_view_function(request, club_pk, *args):
        try:
            club = Club.objects.get(pk=club_pk)
        except ObjectDoesNotExist:
            return redirect('club_list')
        else:
            return view_function(request, club_pk, *args)
    return modified_view_function
