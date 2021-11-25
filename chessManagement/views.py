from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from .models import User, Club, UserInClub
from .forms import SignUpForm, LogInForm, changePassword, changeProfile
from .helpers import login_prohibited

club_session = ""


def getClubAccount(user, club_name):
    global club_session
    club = Club.objects.get(name=club_name)
    accounts = UserInClub.objects.filter(club=club)
    if (len(accounts) != 0):
        account = accounts.get(user=user,club=club)
        return account

def home(request):
    return render(request, 'home.html')


@login_required
def change_password(request):
    user = request.user
    if request.method == 'POST':
        form = changePassword(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data.get('new_password'))
            user.save()
            login(request, user)
            return redirect('profile')
    password = changePassword()
    return render(request, 'change_password.html', {'form': password, 'user': user})


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
            return redirect('profile')
    profile = changeProfile(
        initial={'first_name': user.first_name, 'last_name': user.last_name, 'experience': user.experience,
                 'email': user.email, 'bio': user.bio, 'personal_statement': user.personal_statement})
    return render(request, 'change_profile.html', {'form': profile, 'user': user})


@login_prohibited
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('club_list_home')
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
                return redirect('club_list_home')
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    try:
        rank = getClubAccount(user, club_session)
        return render(request, 'profile.html', {'user': user, 'shown_user': rank, 'current_user': rank})
    except ObjectDoesNotExist:
        return render(request, 'profile.html', {'user': user})


def club_profile(request, club_name):
    global club_session
    if "club_home" in request.META['HTTP_REFERER']:
        club_session = club_name
    try:
        club = Club.objects.get(name=club_name)
        accounts = UserInClub.objects.filter(club=club, user=request.user)
        if len(accounts) != 0:
            if club_session == club.name:
                club_account = accounts.get(user=request.user, club=club_name)
                return render(request, 'club_profile.html',
                              {'clubs': club, 'user': club.owner(), 'current_user': club_account, 'applied': True})
            club_account2 = UserInClub.objects.get(user=request.user, club=club_session)
            return render(request, 'club_profile.html',
                          {'clubs': club, 'user': club.owner(), 'applied': True, 'current_user': club_account2})
    except ObjectDoesNotExist:
        pass
    club = Club.objects.get(name=club_name)
    return render(request, 'club_profile.html',
                  {'clubs': club, 'user': club.owner(), 'applied': False, 'current': request.user})


@login_required
def club_list(request):
    try:
        club_account = getClubAccount(request.user, club_session)
        clubs = Club.objects.all()
        return render(request, 'club_list.html', {'clubs': clubs, 'current_user': club_account})
    except ObjectDoesNotExist:
        pass
    clubs = Club.objects.all()
    return render(request, 'club_list.html', {'clubs': clubs})


def club_list_home(request):
    clubs = Club.objects.all()
    return render(request, 'club_list_home.html', {'clubs': clubs})


@login_required
def user_list(request):
    global club_session
    user = request.user
    club_account = getClubAccount(user, club_session)
    if club_account.user_level == 0:
        return render(request, 'page_unavailable.html')
    else:
        users = UserInClub.objects.filter(user_level__in=[1, 2, 3], club=club_account.club)
        return render(request, 'user_list.html', {'users': users, 'current_user': club_account.club})


@login_required
def applicant_list(request):
    global club_session
    user = request.user
    club_account = getClubAccount(user, club_session)
    if club_account.user_level == 0 or club_account.user_level == 1:
        return render(request, 'page_unavailable.html')
    else:
        users = UserInClub.objects.filter(club=club_account.club)
        return render(request, 'applicant_list.html', {'users': users, 'current_user': club_account})


@login_required
def show_user(request, user_id):
    global club_session
    try:
        user = request.user
        club_account = getClubAccount(user, club_session)
        shown_user = User.objects.get(id=user_id)
        club_account2 = getClubAccount(shown_user, club_session)
        if club_account.user_level == 0:
            return render(request, 'page_unavailable.html')
        if club_account.user_level == 1:
            return render(request, 'show_user.html', {'shown_user': club_account2, 'current_user': club_account})
        if club_account.user_level == 2:
            return render(request, 'officer_show_user.html',
                          {'shown_user': club_account2, 'current_user': club_account})
        if club_account.user_level == 3:
            return render(request, 'owner_show_user.html', {'shown_user': club_account2, 'current_user': club_account})
    except ObjectDoesNotExist:
        return redirect('user_list')


@login_required
def to_member(request, user_id):
    global club_session
    try:
        user = request.user
        club_account = getClubAccount(user, club_session)
        shown_user = User.objects.get(id=user_id)
        club_account2 = getClubAccount(shown_user, club_session)
        if (club_account.user_level > 1 and club_account2.user_level == 0) or club_account.user_level == 3:
            club_account2.user_level = 1
            club_account2.save(update_fields=["user_level"])
            return redirect('profile')
    except ObjectDoesNotExist:
        return redirect('applicant_list')


@login_required
def to_officer(request, user_id):
    global club_session
    try:
        user = request.user
        club_account = getClubAccount(user, club_session)
        shown_user = User.objects.get(id=user_id)
        club_account2 = getClubAccount(shown_user, club_session)
        if (club_account2.user_level == 1):
            club_account2.user_level = 2
            club_account2.save(update_fields=["user_level"])
        return redirect('user_list')
    except ObjectDoesNotExist:
        return redirect('user_list')


@login_required
def transfer_ownership(request, user_id):
    global club_session
    try:
        user = request.user
        club_account = getClubAccount(user, club_session)
        shown_user = User.objects.get(id=user_id)
        club_account2 = getClubAccount(shown_user, club_session)
        if (club_account2.user_level == 2 and club_account.user_level == 3):
            club_account2.user_level = 3
            club_account.user_level = 2
            club_account2.save(update_fields=["user_level"])
            club_account.save(update_fields=["user_level"])
        return redirect('user_list')
    except ObjectDoesNotExist:
        return redirect('user_list')


@login_required
def club_Application(request, user_id,club_name):
    try:
        user = User.objects.get(id=user_id)
        club = Club.objects.get(name=club_name)
        accounts = UserInClub.objects.filter(club=club, user=user)
        if len(accounts) == 0:
            new_applicant = UserInClub.objects.create(
                user=user,
                club=club,
                user_level=0
            )
            new_applicant.save()
        return redirect('profile')
    except ObjectDoesNotExist:
        return redirect('profile')
