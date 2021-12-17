import datetime
from typing import OrderedDict
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from faker import Faker
from faker.providers import BaseProvider
from faker.providers import address, date_time
from chessManagement.models import Tournament, User, Club, UserInClub, UserInTournament
from random import randint, random

class Command(BaseCommand):
    PASSWORD = "Password123"
    USER_COUNT = 50
    CLUB_COUNT = 5
    USER_IN_CLUB_PROBABILITY = 0.8
    ORGANISER_CREATE_TOURNAMENT_PROBABILITY = 0.1
    USER_IN_TOURNAMENT_PROBABILITY = 0.2

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self._create_samples()
        self.create_users()
        self.users = User.objects.all()
        self._create_clubs()
        self.clubs = Club.objects.all()
        self._create_usersInClubs()
        self.usersInClubs = UserInClub.objects.all()
        self._create_tournaments()
        self.tournaments = Tournament.objects.all()
        self._create_usersInTournaments()

    def create_users(self):
        user_count = 3
        while user_count < self.USER_COUNT:
            print(f"Seeding user {user_count}/{self.USER_COUNT}", end='\r')
            try:
                user = self._create_user()
            except:
                continue
            user_count += 1
        print("User seeding complete.      ")

    def _create_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = self._email(first_name, last_name)
        username = email
        bio = self.faker.text(max_nb_chars=520)
        personal_statement = self.faker.text(max_nb_chars=500)
        experience = self.faker.random_choices(elements=('Beginner', 'Intermediate', 'Master'), length=1)[0]
        User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=Command.PASSWORD,
            bio=bio,
            personal_statement=personal_statement,
            experience=experience
        )

    def _create_clubs(self):
        club_count = 1
        while club_count < self.CLUB_COUNT:
            print(f"Seeding club {club_count}/{self.CLUB_COUNT}", end='\r')
            try:
                club = self._create_club()
            except:
                continue
            club_count += 1
        print("Club seeding complete.      ")

    def _create_club(self):
        location = self.faker.city()
        name = self._club_name(location)
        description = self.faker.text(max_nb_chars=520)
        club = Club.objects.create(
            name=name,
            location=location,
            description=description
        )

    def _create_usersInClubs(self):
        userInClub_count = 3
        for club in self.clubs:
            print(f"Seeding userInClub {userInClub_count}/{self.CLUB_COUNT*self.USER_COUNT}", end='\r')
            self._create_owner_userInClub(club)
            userInClub_count += 1
            for user in self.users:
                try:
                    self._create_userInClub(user, club)
                except:
                    continue
                userInClub_count += 1
        print("UserInClub seeding complete.      ")

    def _create_owner_userInClub(self, club):
        user = self.get_random_user()
        UserInClub.objects.create(
            user=user,
            club=club,
            user_level=3
        )

    def get_random_user(self):
        index = randint(0,self.users.count()-1)
        return self.users[index]

    def _create_userInClub(self, user, club):
        if random() < self.USER_IN_CLUB_PROBABILITY:
            user_level = self.faker.random_int(min=0, max=2)
            UserInClub.objects.create(
                user=user,
                club=club,
                user_level=user_level
            )

    def _create_tournaments(self):
        tournament_count = 2
        for club in self.clubs:
            user_ids = self.usersInClubs.filter(club=club,user_level__in=[2,3]).values_list('user', flat=True)
            organisers = User.objects.filter(id__in=user_ids)
            for organiser in organisers:
                print(f"Seeding tournament {tournament_count}", end='\r')
                try:
                    self._create_tournament(club, organiser)
                except:
                    continue
                tournament_count += 1
        print("Tournament seeding complete.      ")

    def _create_tournament(self, club, organiser):
        if random() < self.ORGANISER_CREATE_TOURNAMENT_PROBABILITY:
            name = f'{organiser.first_name} {organiser.last_name} Tournament'
            description = self.faker.text(max_nb_chars=520)
            max_players = self.faker.random_int(min=2, max=96)
            deadline = self.faker.date_this_month(before_today=True, after_today=True)
            tournament = Tournament.objects.create(
                name=name,
                club=club,
                description=description,
                organiser=organiser,
                max_players=max_players,
                deadline=deadline,
                finished=False
            )
            UserInTournament.objects.create(
                user=organiser,
                tournament=tournament,
                is_organiser=True,
                is_co_organiser=False
            )

    def _create_usersInTournaments(self):
        userInTournaments_count = 0
        for tournament in self.tournaments:
            user_ids = self.usersInClubs.filter(club=tournament.club,user_level__in=[1,2,3]).values_list('user', flat=True)
            users = User.objects.filter(id__in=user_ids)
            for user in users:
                if (user.username == 'jeb@example.org') and (tournament.name == 'Valentina Tournament Before Deadline'):
                    continue
                print(f"Seeding userInTournament {userInTournaments_count}", end='\r')
                if not user == tournament.organiser:
                    try:
                        self._create_userInTournament(user, tournament)
                    except:
                        continue
                    userInTournaments_count += 1
        print("UserInTournaments seeding complete.      ")
    
    def _create_userInTournament(self, user, tournament):
        if (user.username == 'jeb@example.org' and tournament.name == "Valentina Tournament After Deadline") or (random() < self.USER_IN_TOURNAMENT_PROBABILITY):
            is_co_organiser = self.faker.random_elements(elements=OrderedDict([("True", 0.05), ("False", 0.95), ]), length=1)[0]
            UserInTournament.objects.create(
                    user=user,
                    tournament=tournament,
                    is_organiser=False,
                    is_co_organiser=is_co_organiser
                )

    def _create_samples(self):
        bio = self.faker.text(max_nb_chars=520)
        personal_statement = self.faker.text(max_nb_chars=500)
        experience = self.faker.random_choices(elements=('Beginner', 'Intermediate', 'Master'), length=1)[0]
        Jebediah = User.objects.create_user(
            first_name='Jebediah',
            last_name='Kerman',
            email='jeb@example.org',
            username='jeb@example.org',
            password=Command.PASSWORD,
            bio=bio,
            personal_statement=personal_statement,
            experience=experience
        )
        Valentina = User.objects.create_user(
            first_name='Valentina',
            last_name='Kerman',
            email='val@example.org',
            username='val@example.org',
            password=Command.PASSWORD,
            bio=bio,
            personal_statement=personal_statement,
            experience=experience
        )
        Billie = User.objects.create_user(
            first_name='Billie',
            last_name='Kerman',
            email='billie@example.org',
            username='billie@example.org',
            password=Command.PASSWORD,
            bio=bio,
            personal_statement=personal_statement,
            experience=experience
        )

        location = self.faker.city()
        club_description = self.faker.text(max_nb_chars=520)
        club = Club.objects.create(
            name='Kerbal Chess Club',
            location=location,
            description=club_description
        )

        UserInClub.objects.create(
            user=Billie,
            club=club,
            user_level=3
        )

        UserInClub.objects.create(
            user=Valentina,
            club=club,
            user_level=2
        )

        UserInClub.objects.create(
            user=Jebediah,
            club=club,
            user_level=1
        )

        tournament_description = self.faker.text(max_nb_chars=520)
        max_players = self.faker.random_int(min=2, max=96)
        tournament_before_deadline = Tournament.objects.create(
                name="Valentina Tournament Before Deadline",
                club=club,
                description=tournament_description,
                organiser=Valentina,
                max_players=max_players,
                deadline=datetime.datetime.now() + datetime.timedelta(days=1),
                finished=False
        )

        UserInTournament.objects.create(
                user=Valentina,
                tournament=tournament_before_deadline,
                is_organiser=True,
                is_co_organiser=False
        )

        tournament_passed_deadline = Tournament.objects.create(
                name="Valentina Tournament After Deadline",
                club=club,
                description=tournament_description,
                organiser=Valentina,
                max_players=max_players,
                deadline=self.faker.date_this_month(before_today=True, after_today=False),
                finished=False
        )

        UserInTournament.objects.create(
                user=Valentina,
                tournament=tournament_passed_deadline,
                is_organiser=True,
                is_co_organiser=False
        )
        print("Sample creating complete.      ")

    def _email(self, first_name, last_name):
        email = f'{first_name}.{last_name}@example.org'
        return email
    
    def _club_name(self, location):
        name = f'{location} Chess Club'
        return name