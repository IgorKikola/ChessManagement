from django.core.management.base import BaseCommand, CommandError
from chessManagement.models import Tournament, User, Club, UserInClub, UserInTournament, Stage, Game, Group

class Command(BaseCommand):
    def handle(self, *args, **options):
        Game.objects.all().delete()
        Stage.objects.all().delete()
        Group.objects.all().delete()
        UserInTournament.objects.all().delete()
        Tournament.objects.all().delete()
        UserInClub.objects.all().delete()
        Club.objects.all().delete()
        User.objects.filter(is_staff=False, is_superuser=False).delete()