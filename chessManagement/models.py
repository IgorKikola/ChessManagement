from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser
from libgravatar import Gravatar


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    # USER_TYPE_CHOICES = (
    #       (1, 'applicant'),
    #       (2, 'member'),
    #       (3, 'officer'),
    #       (4, 'owner'),
    # )
    #
    # user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)

    APPLICANT = 0
    MEMBER = 1
    OFFICER = 2
    OWNER = 3
    USER_LEVEL_CHOICES = (
        (APPLICANT, "Applicant"),
        (MEMBER, "Member"),
        (OFFICER, "Officer"),
        (OWNER, "Owner"),
    )
    user_level = models.CharField(max_length=50 ,blank=False, choices=USER_LEVEL_CHOICES, default=APPLICANT)

    #lol_name = models.CharField(max_length=50 ,blank=False)

    CHESS_CHOICES = (
        ('Beginner', 'beginner'),
        ('Intermediate', 'intermediate'),
        ('Master', 'master'),
    )
    first_name = models.CharField(max_length=50 ,blank=False)
    last_name = models.CharField(max_length=50 ,blank=False)
    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=520 ,blank=True)
    experience = models.CharField(max_length=300,choices=CHESS_CHOICES)
    personal_statement = models.CharField(max_length=500 ,blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""
        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        return self.gravatar(size=60)
