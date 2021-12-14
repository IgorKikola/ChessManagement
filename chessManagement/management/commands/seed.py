from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from faker import Faker
from faker.providers import BaseProvider
from faker.providers import address
from chessManagement.models import User, Club, UserInClub
from random import randint, random

class Command(BaseCommand):
    PASSWORD = "Password123"
    USER_COUNT = 100
    CLUB_COUNT = 10
    INCLUB_PROBABILITY = 0.5

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self._create_samples()
        self.create_users()
        self.users = User.objects.all()
        self._create_clubs()
        self._create_usersInClubs()

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
        clubs = Club.objects.all()
        for club in clubs:
            self._create_owner_userInClub(club)
            users = User.objects.all()
            for user in users:
                print(f"Seeding userInClub {userInClub_count}/{self.CLUB_COUNT*self.USER_COUNT}", end='\r')
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
        if random() < self.INCLUB_PROBABILITY:
            user_level = self.faker.random_int(min=0, max=2)
            UserInClub.objects.create(
                user=user,
                club=club,
                user_level=user_level
            )

    def _create_samples(self):
        if (User.objects.filter(username='jeb@example.org').count())!=0:
            return
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
        description = self.faker.text(max_nb_chars=520)
        club = Club.objects.create(
            name='Kerbal Chess Club',
            location=location,
            description=description
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
        print("Sample creating complete.      ")

    def _email(self, first_name, last_name):
        email = f'{first_name}.{last_name}@example.org'
        return email
    
    def _club_name(self, location):
        name = f'{location} Chess Club'
        return name