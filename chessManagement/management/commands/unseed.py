from django.core.management.base import BaseCommand, CommandError
from chessManagement.models import User, Club, UserInClub

class Command(BaseCommand):
    def handle(self, *args, **options):
        UserInClub.objects.all().delete()
        User.objects.filter(is_staff=False, is_superuser=False).delete()
        Club.objects.all().delete()
