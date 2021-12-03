from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from .models import User, Club, UserInClub
from .forms import SignUpForm, LogInForm, changePassword, changeProfile, createClubForm, changeClubDetails
from .helpers import login_prohibited

club_pk = ""
@login_prohibited
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
            return redirect('profile')
    profile = changeProfile(initial={'first_name': user.first_name,'last_name': user.last_name,'experience': user.experience ,'email': user.email,'bio': user.bio, 'personal_statement': user.personal_statement})
    return render(request, 'change_profile.html', {'form': profile, 'user' :user})

@login_prohibited
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
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
                return redirect('profile')
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
            return redirect('profile')
    else:
        form = createClubForm()
    return render(request,'create_club.html',{'form':form})

@login_required
def club_list(request):
    clubs = Club.objects.all()
    return render(request, 'club_list.html', {'clubs': clubs})

@login_required
def show_club(request, pk=None):
    flag_applicants = 0
    applied = False
    try:
        global club_pk
        club_pk=pk
        club = Club.objects.get(pk=pk)
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
        template = templates[account.first().user_level]

        return render(request, template, {'club': club, 'users': usersInClub, 'flag_applicants':flag_applicants,'applied':applied})

@login_required
def apply_Club(request,pk=None):
    global club_pk
    try:
        global club_pk
        club_pk = pk
        user = request.user
        club = Club.objects.get(pk=pk)
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

@login_required
def owner_manage_club_list(request):
    user = request.user
    ownClubs = user.ownClubs
    return render(request, 'owner_manage_club_list.html', {'clubs': ownClubs})

@login_required
def owner_manage_club(request, pk=None):
    flag_applicants = 1
    try:
        global club_pk
        club_pk=pk
        club = Club.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return redirect('owner_manage_club_list.html')
    else:
        usersInClub = club.members
        return render(request, 'owner_manage_club.html',{'club': club, 'users': usersInClub, 'flag_applicants':flag_applicants})

@login_required
def officer_manage_club_list(request):
    user = request.user
    officerClubs = user.OfficerOfClubs
    return render(request, 'officer_manage_club_list.html', {'clubs': officerClubs})

@login_required
def officer_manage_club(request, pk=None):
    flag_applicants = 1
    try:
        global club_pk
        club_pk=pk
        club = Club.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return redirect('officer_manage_club_list.html')
    else:
        usersInClub = club.members
        return render(request, 'officer_manage_club.html',{'club': club, 'users': usersInClub, 'flag_applicants':flag_applicants})

@login_required
def member_manage_club_list(request):
    user = request.user
    memberClubs = user.clubsMemberOf
    return render(request, 'member_manage_club_list.html', {'clubs': memberClubs})

@login_required
def member_manage_club(request, pk=None):
    flag_applicants = 0
    try:
        global club_pk
        club_pk=pk
        club = Club.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return redirect('member_manage_club_list.html')
    else:
        usersInClub = club.members
        return render(request, 'member_manage_club.html',{'club': club, 'users': usersInClub, 'flag_applicants':flag_applicants})

@login_required
def applicant_manage_club_list(request):
    user = request.user
    memberClubs = user.clubsAppliedTo
    return render(request, 'applicant_manage_club_list.html', {'clubs': memberClubs})

@login_required
def applicant_manage_club(request, pk=None):
    flag_applicants = 0
    try:
        global club_pk
        club_pk=pk
        club = Club.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return redirect('applicant_manage_club_list.html')
    else:
        usersInClub = club.members
        return render(request, 'applicant_manage_club.html',{'club': club, 'users': usersInClub, 'flag_applicants':flag_applicants})

@login_required
def applicant_list(request):
    try:
        global club_pk
        club = Club.objects.get(pk=club_pk)
        allUsers = club.users()
    except ObjectDoesNotExist:
        return redirect('profile')  #just make it easy
    else:
        users = list(allUsers)
        for user in allUsers:
            if not user.isApplicantIn(club):
                users.remove(user)
        return render(request, 'applicant_list.html', {'users': users})

@login_required
def show_user(request, user_id):
    user_self = request.user
    try:
        global club_pk
        club = Club.objects.get(pk=club_pk)
        users = club.users()
    except ObjectDoesNotExist:
        return redirect('club_list')
    else:
        shown_user = users.get(id=user_id)
        rank = shown_user.getRank(club)
        args = {'user': user_self, 'shown_user': shown_user, 'club': club, 'rank': rank}
        if shown_user==user_self:
            return render(request, 'officer_show_user.html', args)
        if user_self.isMemberOf(club):
            return render(request, 'show_user.html', args)
        if user_self.isOfficerOf(club):
            return render(request, 'officer_show_user.html', args)
        if user_self.isOwnerOf(club):
            return render(request, 'owner_show_user.html', args)
        else:
            return render(request, 'page_unavailable.html')

@login_required
def applicant_show_user(request, user_id):
    try:
        global club_pk
        club = Club.objects.get(pk=club_pk)
        users = club.applicants()
    except ObjectDoesNotExist:
        return redirect('club_list')
    else:
        shown_user = users.get(id=user_id)
        rank = shown_user.getRank(club)
        return render(request, 'applicant_show_user.html', {'shown_user': shown_user, 'club': club, 'rank': rank})

@login_required
def manage_owner_show_user(request, user_id):
    try:
        global club_pk
        club = Club.objects.get(pk=club_pk)
        users = club.members()
    except ObjectDoesNotExist:
        return redirect('club_list')
    else:
        shown_user = users.get(id=user_id)
        rank = shown_user.getRank(club)
        return render(request, 'manage_owner_show_user.html', {'shown_user': shown_user, 'club': club, 'rank': rank})

@login_required
def to_member(request, user_id):
    try:
        global club_pk
        club = Club.objects.get(pk=club_pk)
        user = User.objects.get(id=user_id)
        userInClub = club.getUserInClub(user)
    except ObjectDoesNotExist:
        return redirect('club_list')
    else:
        previous_rank = userInClub.user_level
        userInClub.user_level=1
        userInClub.save(update_fields=["user_level"])
        if previous_rank == 2:
            return redirect('show_user', user_id)
        else:
            return redirect('applicant_list')

@login_required
def to_officer(request, user_id):
    try:
        global club_pk
        club = Club.objects.get(pk=club_pk)
        user = User.objects.get(id=user_id)
        userInClub = club.getUserInClub(user)
    except ObjectDoesNotExist:
        return redirect('club_list')
    else:
        if userInClub.user_level==1:
            userInClub.user_level=2
        userInClub.save(update_fields=["user_level"])
        return redirect('show_user', user_id)

@login_required
def transfer_ownership(request, user_id):
    try:
        global club_pk
        club = Club.objects.get(pk=club_pk)
        user = User.objects.get(id=user_id)
        userInClub = club.getUserInClub(user)
    except ObjectDoesNotExist:
        return redirect('club_list')
    else:
        owner = request.user
        ownerInClub = club.getUserInClub(owner)
        if userInClub.user_level==2:
            userInClub.user_level=3
            ownerInClub.user_level=2
            userInClub.save(update_fields=["user_level"])
            ownerInClub.save(update_fields=["user_level"])
        return redirect('show_user', user_id)


def change_club_details(request, pk):
    club = Club.objects.get(pk=pk)
    if request.user != club.owner():
        return redirect('show_club', pk=pk)
    else:
        if request.method == 'POST':
            form = changeClubDetails(request.POST)
            if form.is_valid():
                club.location = form.cleaned_data.get('location')
                club.description = form.cleaned_data.get('description')
                club.save()
                return redirect('owner_manage_club', pk=pk)
        clubDetails = changeClubDetails(initial={'location': club.location, 'description': club.description})
        return render(request, 'change_club_details.html', {'form': clubDetails, 'club': club})
