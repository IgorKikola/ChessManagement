from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from faker import Faker
from faker.providers import BaseProvider
from faker.providers import address
from chessManagement.models import User, Club, UserInClub

class Command(BaseCommand):
    PASSWORD = "Password123"
    USER_COUNT = 50
    CLUB_COUNT = 4

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        user_count = 0
        club_count = 0
        while user_count < Command.USER_COUNT:
            print(f'Seeding user {user_count}',  end='\r')
            try:
                user = self._create_user()
            except (IntegrityError):
                continue
            user_count += 1

        while club_count < Command.CLUB_COUNT:
            print(f'Seeding club {club_count}',  end='\r')
            try:
                club = self._create_club()
            except (IntegrityError):
                continue
            club_count += 1
            users = User.objects.all()
            for user in users:
                try:
                    self._create_userInClub(user, club)
                except (IntegrityError):
                    continue
        print('User, club, and userInClub seeding complete')

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

    def _email(self, first_name, last_name):
        email = f'{first_name}.{last_name}@example.org'
        return email

    def _create_club(self):
        name = self.faker.random_elements(elements=('Kerbal Chess Club', 'AA Chess Club', 'BB Chess Club', 'CC Chess Club'), length=1, unique=True)[0]
        location = self.faker.city()
        description = self.faker.text(max_nb_chars=520)
        club = Club.objects.create(
            name=name,
            location=location,
            description=description
        )
        return club

    def _create_userInClub(self, user, club):
        owner_id = UserInClub.objects.filter(club=club,user_level__in=[3]).values_list('user', flat=True)
        if User.objects.filter(id__in=owner_id).count()==0:
            UserInClub.objects.create(
                user=user,
                club=club,
                user_level=3
            )
        else:
            user_level = self.faker.random_int(min=0, max=2)
            UserInClub.objects.create(
                user=user,
                club=club,
                user_level=user_level
            )
