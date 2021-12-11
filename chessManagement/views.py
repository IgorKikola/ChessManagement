import datetime

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import User, Club, UserInClub, Tournament, UserInTournament
from .forms import SignUpForm, LogInForm, changePassword, changeProfile, createClubForm, changeClubDetails, \
    createTournamentForm
from .helpers import login_prohibited
from django.contrib import messages

@login_prohibited
def home(request):
    return render(request, 'home.html')

@login_required
def create_tournament(request,club_pk):
    user = request.user
    if request.method == 'POST':
        form = createTournamentForm(request.POST)
        if form.is_valid():
            club = Club.objects.get(pk=club_pk)
            tournament = form.save(request.user,club)
            return redirect('profile')
    else:
        form = createTournamentForm()
    return render(request,'create_tournament.html',{'form':form,'club_pk':club_pk})

@login_required
def tournament_list(request,club_pk):
    club = Club.objects.get(pk=club_pk)
    tournament = Tournament.objects.all().filter(club=club)
    return render(request, 'tournament_list.html', {'tournaments': tournament})

@login_required#
def officer_list(request,tournament_pk):
    tournament = Tournament.objects.get(pk=tournament_pk)
    officers = UserInClub.objects.all().filter(club=tournament.club,user_level=2)
    request_user = UserInTournament.objects.get(user=request.user,tournament=tournament_pk)
    non_co_organisers=[]
    for officer in officers:
        accounts = UserInTournament.objects.filter(tournament=tournament, user=officer.user,is_co_organiser=True)
        if len(accounts) == 0:
            non_co_organisers.append(officer)
    return render(request, 'tournament_users/officer_list.html', {'officers': non_co_organisers,'tournament_pk':tournament_pk,'request_user':request_user})

@login_required#
def co_organiser_list(request,tournament_pk):
    tournament = Tournament.objects.get(pk=tournament_pk)
    co_organisers = UserInTournament.objects.filter(tournament=tournament,is_co_organiser=True)
    request_user = UserInTournament.objects.get(user=request.user,tournament=tournament)
    return render(request, 'tournament_users/co_organiser_list.html', {'co_organisers': co_organisers,'tournament_pk':tournament_pk,'request_user':request_user})

@login_required#
def allow_co_organiser(request, tournament_pk,user_id):
    try:
        user = User.objects.get(id=user_id)
        tournament = Tournament.objects.get(pk=tournament_pk)
        accounts = UserInTournament.objects.filter(tournament=tournament, user=user)
        if len(accounts) == 0:
            new_applicant = UserInTournament.objects.create(
                user=user,
                tournament=tournament,
                is_organiser=False,
                is_co_organiser=True
            )
            new_applicant.save()
            return redirect(officer_list,tournament_pk)
        return redirect(officer_list,tournament_pk)
    except ObjectDoesNotExist:
        return redirect(officer_list,tournament_pk)

@login_required#
def remove_co_organiser(request, tournament_pk,user_id):
    try:
        user = User.objects.get(id=user_id)
        tournament = Tournament.objects.get(pk=tournament_pk)
        accounts = UserInTournament.objects.filter(tournament=tournament, user=user)
        if len(accounts) != 0:
            UserInTournament.objects.get(tournament=tournament,user=user,is_co_organiser=True).delete()
        return redirect(co_organiser_list,tournament_pk)
    except ObjectDoesNotExist:
        return redirect(co_organiser_list,tournament_pk)

@login_required#
def sign_up_tournament(request, tournament_pk):
    try:
        user = request.user
        tournament = Tournament.objects.get(pk=tournament_pk)
        players = UserInTournament.objects.filter(tournament=tournament,is_organiser=False).count()
        if players <= tournament.max_players:
            accounts = UserInTournament.objects.filter(tournament=tournament, user=user)
            if len(accounts) == 0:
                new_applicant = UserInTournament.objects.create(
                    user=user,
                    tournament=tournament,
                    is_organiser=False,
                    is_co_organiser=False
                )
                new_applicant.save()
        return redirect('show_tournament', tournament.club.pk, tournament.pk)
    except ObjectDoesNotExist:
        return redirect('profile')

@login_required#
def cancel_sign_up_tournament(request, tournament_pk):
    try:
        user = request.user
        tournament = Tournament.objects.get(pk=tournament_pk)
        accounts = UserInTournament.objects.filter(tournament=tournament, user=user)
        if len(accounts) != 0:
            UserInTournament.objects.get(tournament=tournament,user=user).delete()
        return redirect('show_tournament', tournament.club.pk, tournament.pk)
    except ObjectDoesNotExist:
        return redirect('profile')

@login_required
def show_tournament(request,club_pk,tournament_pk):
    expired = False
    applied = False
    try:
        tournament = Tournament.objects.get(pk=tournament_pk)
        if tournament.deadline < datetime.date.today():
            expired = True
        account = UserInTournament.objects.filter(tournament=tournament, user=request.user)
        if len(account) != 0:
            user = UserInTournament.objects.get(tournament=tournament, user=request.user)
            applied = True
    except ObjectDoesNotExist:
        pass
        return redirect('tournament_list', club_pk)
    else:
        usersIntournament = tournament.users()

        templates = {
            0: 'show_tournament/for_organiser.html',
            1: 'show_tournament/for_members.html',
        }
        if applied:
            template = templates[1]
            if user.is_organiser or user.is_co_organiser:
                template = templates[0]
        else:
            template = templates[1]
        return render(request, template, {'tournament': tournament, 'users': usersIntournament, 'applied': applied,'expired':expired})

@login_required
def change_password(request):
    user = request.user
    if request.method == 'POST':
        form = changePassword(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data.get('new_password'))
            user.save()
            login(request, user)
            messages.add_message(request, messages.SUCCESS, "Password changed!")
            return redirect('profile')
        messages.add_message(request, messages.ERROR, "Passwords did not match!")
    password = changePassword()
    return render(request, 'change_password.html', {'form': password, 'user' :user})

@login_required
def change_profile(request):
    user = request.user
    if request.method == 'POST':
        form = changeProfile(request.POST)
        if form.is_valid():
            if (form.data['first_name']):
                user.first_name = form.cleaned_data.get('first_name')
            if (form.data['last_name']):
                user.last_name = form.cleaned_data.get('last_name')
            if (form.data['email']):
                user.email = form.cleaned_data.get('email')
                user.username = form.cleaned_data.get('email')
            user.bio = form.cleaned_data.get('bio')
            user.personal_statement = form.cleaned_data.get('personal_statement')
            user.experience = form.cleaned_data.get('experience')
            user.save()
            messages.add_message(request, messages.SUCCESS, "Profile information changed!")
            return redirect('profile')
        messages.add_message(request, messages.ERROR, "Something was invalid!")
    profile = changeProfile(initial={'first_name': user.first_name,'last_name': user.last_name,'experience': user.experience ,'email': user.email,'bio': user.bio, 'personal_statement': user.personal_statement})
    return render(request, 'change_profile.html', {'form': profile, 'user' :user})

@login_prohibited
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.add_message(request, messages.SUCCESS, "Successfully signed up!")
            return redirect('profile')
        messages.add_message(request, messages.ERROR, "Something wasn't right!")
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('home')

@login_prohibited
def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, "Logged in!")
                return redirect('profile')
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    clubsIn = user.clubsIn
    clubsAppliedTo = user.clubsAppliedTo
    return render(request, 'profile.html', {'user': user, 'clubsIn': clubsIn, 'clubsAppliedTo': clubsAppliedTo})


@login_required
def create_club(request):
    if request.method == 'POST':
        form = createClubForm(request.POST)
        if form.is_valid():
            club = form.save(request.user)
            messages.add_message(request, messages.SUCCESS, "Successfully created club!")
            return redirect('profile')
        messages.add_message(request, messages.ERROR, "Something wasn't right!")
    else:
        form = createClubForm()
    return render(request,'create_club.html',{'form':form})

@login_required
def club_list(request):
    clubs = Club.objects.all()
    return render(request, 'club_list/all.html', {'clubs': clubs})

@login_required
def clubs_applied_to_list(request):
    user = request.user
    clubs = user.clubsAppliedTo()
    return render(request, 'club_list/applied_to.html', {'clubs': clubs})

@login_required
def clubs_joined_list(request):
    user = request.user
    clubs = user.clubsIn()
    return render(request, 'club_list/joined.html', {'clubs': clubs})

@login_required
def show_club(request, club_pk):
    applied = False
    try:
        club = Club.objects.get(pk=club_pk)
        account = UserInClub.objects.filter(club=club, user=request.user)
        if len(account) != 0:
            applied = True
    except ObjectDoesNotExist:
        return redirect('club_list')
    else:
        usersInClub = club.members

        templates = {
            0: 'show_club/for_applicant.html',
            1: 'show_club/for_member.html',
            2: 'show_club/for_officer.html',
            3: 'show_club/for_owner.html',
        }
        if applied:
            template = templates[account.first().user_level]
        else:
            template = templates[0]

        return render(request, template, {'club': club, 'users': usersInClub, 'applied': applied})

@login_required
def apply_Club(request, club_pk):
    try:
        user = request.user
        club = Club.objects.get(pk=club_pk)
        accounts = UserInClub.objects.filter(club=club, user=user)
        if len(accounts) == 0:
            new_applicant = UserInClub.objects.create(
                user=user,
                club=club,
                user_level=0
            )
            new_applicant.save()
        return redirect('show_club', club_pk)
    except ObjectDoesNotExist:
        return redirect('profile')


@login_required
def applicant_list(request, club_pk):
    try:
        club = Club.objects.get(pk=club_pk)
        allUsers = club.users()
    except ObjectDoesNotExist:
        return redirect('club_list')
    try:
        session_user_in_club = club.getUserInClub(request.user)
    except ObjectDoesNotExist:
        return redirect('show_club', club_pk)
    else:
        if session_user_in_club.user_level == 0 or session_user_in_club.user_level == 1:
            return redirect('show_club', club_pk)
        users = list(allUsers)
        for user in allUsers:
            if not user.isApplicantIn(club):
                users.remove(user)
        return render(request, 'applicant_list.html', {'users': users, 'club': club})

@login_required
def show_user(request, user_id, club_pk):
    session_user = request.user
    try:
        club = Club.objects.get(pk=club_pk)
    except ObjectDoesNotExist:
        return redirect('club_list')
    try:
        shown_user_in_club = club.getUserInClub(user_id)
        session_user_in_club = club.getUserInClub(session_user)
    except ObjectDoesNotExist:
        return redirect('show_club', club_pk)
    else:
        if session_user_in_club.isApplicant():
            return redirect('show_club', club_pk)
        elif shown_user_in_club.isApplicant() and session_user_in_club.isOfficer():
            return render(request, 'show_applicant.html', {'user': session_user, 'shown_user': shown_user_in_club.user, 'club': club, 'user_rank': "Applicant"})
        elif shown_user_in_club.isMember() and session_user_in_club.isMember():

            if shown_user_in_club == session_user_in_club:
                return redirect('profile')

            session_user_rank = session_user_in_club.user_level
            shown_user_rank = shown_user_in_club.user_level

            templates = {
                1: 'show_member/for_member.html',
                2: 'show_member/for_officer.html',
                3: 'show_member/for_owner.html',
            }
            template = templates[session_user_rank]

            return render(request, template, {'user': session_user, 'shown_user': shown_user_in_club.user, 'club': club, 'user_rank': shown_user_in_club.rankToString()})
        else:
            return redirect('show_club', club_pk)

@login_required
def to_member(request, user_id, club_pk):
    try:
        club = Club.objects.get(pk=club_pk)
        user = User.objects.get(id=user_id)
        userInClub = club.getUserInClub(user)
    except ObjectDoesNotExist:
        return redirect('club_list')
    else:
        if request.user.isOfficerOf(club) or request.user.isOwnerOf(club):
            previous_rank = userInClub.user_level
            userInClub.user_level=1
            userInClub.save(update_fields=["user_level"])
            if previous_rank == 2:
                return redirect('show_user', club_pk, user_id)
            else:
                return redirect('applicants', club_pk)
        return redirect('show_club', club_pk)

@login_required
def to_officer(request, user_id, club_pk):
    try:
        club = Club.objects.get(pk=club_pk)
        user = User.objects.get(id=user_id)
        userInClub = club.getUserInClub(user)
    except ObjectDoesNotExist:
        return redirect('club_list')
    else:
        if request.user.isOwnerOf(club):
            if userInClub.user_level==1:
                userInClub.user_level=2
            userInClub.save(update_fields=["user_level"])
            return redirect('show_user', club_pk, user_id)
        return redirect('show_club', club_pk)

@login_required
def transfer_ownership(request, user_id, club_pk):
    try:
        club = Club.objects.get(pk=club_pk)
        user = User.objects.get(id=user_id)
        userInClub = club.getUserInClub(user)
    except ObjectDoesNotExist:
        return redirect('club_list')
    else:
        if request.user.isOwnerOf(club):
            ownerInClub = club.getUserInClub(request.user)
            if userInClub.user_level==2:
                userInClub.user_level=3
                ownerInClub.user_level=2
                userInClub.save(update_fields=["user_level"])
                ownerInClub.save(update_fields=["user_level"])
            return redirect('show_user', club_pk, user_id)
        return redirect('show_club', club_pk)

@login_required
def change_club_details(request, club_pk):
    club = Club.objects.get(pk=club_pk)
    if request.user != club.owner():
        return redirect('show_club', club_pk)
    else:
        if request.method == 'POST':
            form = changeClubDetails(request.POST)
            if form.is_valid():
                club.location = form.cleaned_data.get('location')
                club.description = form.cleaned_data.get('description')
                club.save()
                return redirect('show_club', club_pk)
        clubDetails = changeClubDetails(initial={'location': club.location, 'description': club.description})
        return render(request, 'change_club_details.html', {'form': clubDetails, 'club': club})


@login_required
def leave_club(request, club_pk):
    try:
        club = Club.objects.get(pk=club_pk)
    except ObjectDoesNotExist:
        return redirect('club_list')
    try:
        userInClub = club.getUserInClub(request.user)
    except ObjectDoesNotExist:
        return redirect('show_club', club_pk)
    else:
        if not request.user.isOwnerOf(club):
            userInClub.delete()
        return redirect('show_club', club_pk)

@login_required
def delete_club(request, club_pk):
    try:
        club = Club.objects.get(pk=club_pk)
    except ObjectDoesNotExist:
        return redirect('club_list')
    else:
        if request.user.isOwnerOf(club):
            club.delete()
            return redirect('club_list')
        return redirect('show_club', club_pk)

@login_required
def remove_user(request, user_id, club_pk):
    try:
        club = Club.objects.get(pk=club_pk)
        user_to_remove = User.objects.get(id=user_id)
        userInClub = club.getUserInClub(user_to_remove)
    except ObjectDoesNotExist:
        return redirect('club_list')
    else:
        user = request.user
        user_to_remove_rank = userInClub.user_level
        if (user.isOfficerOf(club) and user_to_remove_rank == 2) or (user == user_to_remove) or (user_to_remove_rank == 3):
            return redirect('show_club', club_pk)
        if user.isOfficerOf(club) or user.isOwnerOf(club):
            userInClub.delete()
            if user_to_remove_rank == 0:
                return redirect('applicants', club_pk)
        return redirect('show_club', club_pk)
