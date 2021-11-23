"""Forms for the microblogs app."""
from django import forms
from django.core.validators import RegexValidator
from .models import User

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
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
        )]
    )


class changeProfile(forms.Form):
    """Form enabling unregistered users to sign up."""
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
