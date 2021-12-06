from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
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

    def clubs(self):
        """Return all clubs the user is in, regardless of rank (including applicant)"""
        club_names = UserInClub.objects.filter(user=self).values_list('club', flat=True)
        return Club.objects.filter(name__in=club_names)

    def ownClubs(self):
        """Return all clubs the user owns"""
        club_names = UserInClub.objects.filter(user=self, user_level=3).values_list('club', flat=True)
        return Club.objects.filter(name__in=club_names)

    def OfficerOfClubs(self):
        """Return all clubs the user is an officer of, but not an owner"""
        club_names = UserInClub.objects.filter(user=self, user_level=2).values_list('club', flat=True)
        return Club.objects.filter(name__in=club_names)

    def clubsAppliedTo(self):
        """Return all clubs the user has applied to and isn't a member of yet"""
        club_names = UserInClub.objects.filter(user=self, user_level=0).values_list('club', flat=True)
        return Club.objects.filter(name__in=club_names)

    def clubsMemberOf(self):
        """Return all clubs the user is a member of, but not an officer/owner"""
        club_names = UserInClub.objects.filter(user=self, user_level=1).values_list('club', flat=True)
        return Club.objects.filter(name__in=club_names)

    def clubsIn(self):
        """Return all clubs the user is a member/officer/owner of"""
        club_names = UserInClub.objects.filter(user=self, user_level__in=[1,2,3]).values_list('club', flat=True)
        return Club.objects.filter(name__in=club_names)

    def isApplicantIn(self, club):
        return UserInClub.objects.filter(user=self, club=club, user_level=0).count() == 1

    def isMemberOf(self, club):
        return UserInClub.objects.filter(user=self, club=club, user_level=1).count() == 1

    def isOfficerOf(self, club):
        return UserInClub.objects.filter(user=self, club=club, user_level=2).count() == 1

    def isOwnerOf(self, club):
        return UserInClub.objects.filter(user=self, club=club, user_level=3).count() == 1

class Club(models.Model):

    name = models.CharField(max_length=50, blank=False, primary_key=True)
    location = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=520, blank=True)

    def users(self):
        user_ids = UserInClub.objects.filter(club=self).values_list('user', flat=True)
        return User.objects.filter(id__in=user_ids)

    def applicants(self):
        user_ids = UserInClub.objects.filter(club=self,user_level=0).values_list('user', flat=True)
        return User.objects.filter(id__in=user_ids)

    def members(self):
        user_ids = UserInClub.objects.filter(club=self,user_level__in=[1,2,3]).values_list('user', flat=True)
        return User.objects.filter(id__in=user_ids)

    def numberOfMembers(self):
        user_ids = UserInClub.objects.filter(club=self,user_level__in=[1,2,3]).values_list('user', flat=True)
        allUsers = User.objects.filter(id__in=user_ids)
        return allUsers.count()

    def officers(self):
        user_ids = UserInClub.objects.filter(club=self,user_level__in=[2,3]).values_list('user', flat=True)
        return User.objects.filter(id__in=user_ids)

    def owner(self):
        return UserInClub.objects.filter(club=self, user_level=3).first().user

    def getUserInClub(self, user):
        return UserInClub.objects.get(club=self, user=user, user_level__in=[0,1,2,3])

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""
        club_owner = self.owner()
        gravatar_object = Gravatar(club_owner.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        return self.gravatar(size=60)


class UserInClub(models.Model):

    class Meta:
        unique_together = ("user", "club")

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)

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
    user_level = models.IntegerField(blank=False, choices=USER_LEVEL_CHOICES, default=APPLICANT)

    club = models.ForeignKey(Club, on_delete=models.CASCADE, blank=False)

    def rankToString(self):
        if self.user_level == 0:
            return "Applicant"
        if self.user_level == 1:
            return "Member"
        if self.user_level == 2:
            return "Officer"
        if self.user_level == 3:
            return "Owner"

    def isApplicant(self):
        return self.user_level == 0

    def isMember(self):
        return self.user_level > 0

    def isOfficer(self):
        return self.user_level > 1

    def isOwner(self):
        return self.user_level == 3

class Tournament(models.Model):
    name = models.CharField(max_length=120)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, blank=False)
    description = models.CharField(max_length=520, blank=True)
    organiser = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    max_players = models.IntegerField(validators=[MinValueValidator(2), MaxValueValidator(96)])
    deadline = models.DateField()
    finished = models.BooleanField()

    def users(self):
        user_ids = UserInTournament.objects.filter(tournament=self,is_organiser=False,is_co_organiser=False).values_list('user', flat=True)
        return User.objects.filter(id__in=user_ids)

    def numberOfMembers(self):
        user_ids = UserInTournament.objects.filter(tournament=self,is_organiser=False,is_co_organiser=False).values_list('user', flat=True)
        allUsers = User.objects.filter(id__in=user_ids)
        return allUsers.count()


class UserInTournament(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, blank=False)
    is_organiser = models.BooleanField()
    is_co_organiser = models.BooleanField(default=False)



class Game(models.Model):
    PLAYER1 = 1
    PLAYER2 = 2
    WINNER_CHOICES = (
        (PLAYER1, "Player 1"),
        (PLAYER2, "Player 2"),
    )
    player1 = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,related_name='set_1')
    player2 = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,related_name='set_2')
    finished = models.BooleanField()
    winner = models.CharField(blank=True, max_length=8,null=True, choices=WINNER_CHOICES, default=None)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)