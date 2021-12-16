from django.conf import settings
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Club, Tournament, User, UserInClub, Game

def login_prohibited(view_function):
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request)
    return modified_view_function

def valid_club_required(view_function):
    def modified_view_function(request, club_pk):
        try:
            club = Club.objects.get(pk=club_pk)
        except ObjectDoesNotExist:
            return redirect('club_list')
        else:
            return view_function(request, club_pk)
    return modified_view_function

def valid_club_and_user_required(view_function):
    def modified_view_function(request, club_pk, user_id):
        print("0")
        try:
            print(1)
            club = Club.objects.get(pk=club_pk)
        except ObjectDoesNotExist:
            print(2)
            return redirect('club_list')
        else:
            try:
                print(3)
                user = club.getUserInClub(user_id)
            except ObjectDoesNotExist:
                print(4)
                return redirect('show_club', club_pk)
            else:
                print(5)
                return view_function(request,club_pk,user_id)
    print(6)
    return modified_view_function

def tournament_must_belong_to_club(view_function):
    def modified_view_function(request, club_pk, tournament_pk):
        try:
            club = Club.objects.get(pk=club_pk)
        except ObjectDoesNotExist:
            return redirect('club_list')
        else:
            try:
                tournament = Tournament.objects.get(pk=tournament_pk)
            except ObjectDoesNotExist:
                return redirect('show_club', club_pk)
            else:
                if tournament.club == club:
                    return view_function(request, club_pk, tournament_pk)
                else:
                    return redirect('show_club', club_pk)
    return modified_view_function

def tournament_and_user_must_belong_to_club(view_function):
    def modified_view_function(request, club_pk, tournament_pk, user_id):
        try:
            club = Club.objects.get(pk=club_pk)
        except ObjectDoesNotExist:
            return redirect('club_list')
        else:
            try:
                tournament = Tournament.objects.get(pk=tournament_pk)
            except ObjectDoesNotExist:
                return redirect('show_club', club_pk)
            else:
                if tournament.club == club:
                    try:
                        user = club.getUserInClub(user_id)
                    except ObjectDoesNotExist:
                        return redirect('show_tournament', club_pk, tournament_pk)
                    else:
                        return view_function(request, club_pk, tournament_pk, user_id)
                else:
                    return redirect('show_club', club_pk)
    return modified_view_function

def tournament_and_game_must_belong_to_club(view_function):
    def modified_view_function(request, club_pk, tournament_pk, game_pk):
        try:
            club = Club.objects.get(pk=club_pk)
        except ObjectDoesNotExist:
            return redirect('club_list')
        else:
            try:
                tournament = Tournament.objects.get(pk=tournament_pk)
            except ObjectDoesNotExist:
                return redirect('show_club', club_pk)
            else:
                if tournament.club == club:
                    try:
                        Game.objects.get(pk=game_pk, tournament=tournament)
                    except ObjectDoesNotExist:
                        return redirect('show_tournament', club_pk, tournament_pk)
                    else:
                        return view_function(request, club_pk, tournament_pk, game_pk)
                else:
                    return redirect('show_club', club_pk)
    return modified_view_function
