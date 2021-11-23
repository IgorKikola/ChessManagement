from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from .models import User
from .forms import SignUpForm, LogInForm, changePassword, changeProfile
from .helpers import login_prohibited

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
    return render(request, 'profile.html', {'user': user})

@login_required
def user_list(request):
    user = request.user
    if user.user_level == 0:
        return render(request, 'page_unavailable.html')
    else:
        users = User.objects.filter(user_level__in=[1,2,3])
        return render(request, 'user_list.html', {'users': users})

@login_required
def applicant_list(request):
    user = request.user
    if user.user_level == 0 or user.user_level == 1:
        return render(request, 'page_unavailable.html')
    else:
        users = User.objects.all()
        return render(request, 'applicant_list.html', {'users': users})

@login_required
def show_user(request, user_id):
    user = request.user
    try:
        shown_user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return redirect('user_list')
    else:
        user_self = request.user
        if user_self.user_level == 0:
            return render(request, 'page_unavailable.html')
        if user_self.user_level == 1:
            return render(request, 'show_user.html', {'user': user, 'shown_user': shown_user})
        if user_self.user_level == 2:
            return render(request, 'officer_show_user.html', {'user': user, 'shown_user': shown_user})
        if user_self.user_level == 3:
            return render(request, 'owner_show_user.html', {'user': user, 'shown_user': shown_user})

@login_required
def to_member(request, user_id):
    officer = request.user
    user = User.objects.get(id=user_id)
    if (officer.user_level > 1 and user.user_level == 0) or officer.user_level == 3:
        user.user_level=1
        user.save(update_fields=["user_level"])
    return redirect('show_user', user.id)

@login_required
def to_officer(request, user_id):
    owner = request.user
    user = User.objects.get(id=user_id)
    if user.user_level == 1:
        user.user_level=2
        user.save(update_fields=["user_level"])
    return redirect('show_user', user.id)

@login_required
def transfer_ownership(request, user_id):
    owner = request.user
    user = User.objects.get(id=user_id)
    if owner.user_level == 3 and user.user_level == 2:
        user.user_level=3
        owner.user_level=2
        user.save(update_fields=["user_level"])
        owner.save(update_fields=["user_level"])
    return redirect('show_user', user.id)
