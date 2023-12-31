"""Forms for the microblogs app."""
import datetime

from django import forms
from django.core.validators import RegexValidator
from .models import User, Club, UserInClub, Tournament, UserInTournament, Game


class LogInForm(forms.Form):
    """Form enabling registered users to log in."""

    email = forms.CharField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())


class SignUpForm(forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'email', 'experience','bio','personal_statement']
        widgets = { 'bio': forms.Textarea(), 'personal_statement': forms.Textarea}

    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')

    def save(self):
        """Create a new user."""

        super().save(commit=False)
        user = User.objects.create_user(
            username=self.cleaned_data.get('email'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            bio=self.cleaned_data.get('bio'),
            email=self.cleaned_data.get('email'),
            experience = self.cleaned_data.get('experience'),
            personal_statement = self.cleaned_data.get('personal_statement'),
            password=self.cleaned_data.get('new_password'),
        )
        return user


class changePassword(forms.ModelForm):
    class Meta:
        """Form options."""

        model = User
        fields = []

    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
        )]
    )

    new_password_confirmation = forms.CharField(
        label='New Password Confirmation',
        widget=forms.PasswordInput()
    )

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        new_password_confirmation = self.cleaned_data.get('new_password_confirmation')
        if new_password != new_password_confirmation:
            self.add_error('new_password_confirmation', 'Confirmation does not match password.')


class changeProfile(forms.Form):
    """Form enabling unregistered users to change their profile."""
    first_name = forms.CharField(
        label=("First name"),
        strip=False,
        required=False
    )
    last_name = forms.CharField(
        label=("Last Name"),
        strip=False,
        required=False
    )
    email = forms.EmailField(
        label=("Email"),
        required=False
    )
    experience = forms.ChoiceField(
        required=False,
        choices=User.CHESS_CHOICES
    )
    bio = forms.CharField(
        label=("bio"),
        strip=False,
        widget=forms.Textarea(),
        required=False
        )
    personal_statement = forms.CharField(
        label=("personal statement"),
        strip=False,
        widget=forms.Textarea(),
        required=False
        )


class createClubForm(forms.ModelForm):
    """Form enabling users to create their own club."""

    class Meta:
        """Form options."""

        model = Club
        fields = ['name','location','description']
        widgets = { 'description': forms.Textarea()}

    def save(self,user):
        """Create a new club."""

        super().save(commit=False)
        club = Club.objects.create(
            name=self.cleaned_data.get('name'),
            location=self.cleaned_data.get('location'),
            description=self.cleaned_data.get('description')
        )
        UserInClub.objects.create(
            user=user,
            user_level=3,
            club=club
        )
        return club


class changeClubDetails(forms.Form):
    """Form enabling club owners to change club details."""
    location = forms.CharField(
        label=("Location"),
        strip=False,
        required=True
    )
    description = forms.CharField(
        label=("New description: "),
        strip=False,
        widget=forms.Textarea(),
        required=False
    )


class createTournamentForm(forms.ModelForm):

    class Meta:
        """Form options."""

        class DateInput(forms.DateInput):
            input_type = 'date'

        model = Tournament
        fields = ['name','description','deadline','max_players']
        widgets = { 'description': forms.Textarea(),'deadline':DateInput()}

    def clean(self):
        cleaned_data = super().clean()
        deadline = cleaned_data.get("deadline")
        if deadline is None:
            self.add_error('deadline', "Deadline should not me empty.")
        else:
            if deadline < datetime.date.today():
                self.add_error('deadline',"Deadline should be later than today.")

    def save(self,user,club):
        """Create a new tournament."""

        super().save(commit=False)
        tournament = Tournament.objects.create(
            name=self.cleaned_data.get('name'),
            club=club,
            description=self.cleaned_data.get('description'),
            deadline=self.cleaned_data.get('deadline'),
            max_players=self.cleaned_data.get('max_players'),
            finished=False,
            organiser=user
        )
        UserInTournament.objects.create(
            user=user,
            tournament=tournament,
            is_organiser=True
        )
        return club


class decideGameOutcome(forms.Form):
    """ Form for deciding the winner of a match """
    winner = forms.ChoiceField(
        required=False,
        choices=Game.WINNER_CHOICES
    )
