from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import authenticate,login
from chessManagement.models import User, Club, UserInClub, Tournament, UserInTournament
from chessManagement.tests.helpers import reverse_with_next
from chessManagement.forms import createClubForm

class TournamentListTest(TestCase):

    fixtures = [
        'chessManagement/tests/fixtures/default_user.json',
        'chessManagement/tests/fixtures/other_users.json',
        'chessManagement/tests/fixtures/default_club.json'
    ]


    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.other_user = User.objects.get(username='janedoe@example.org')
        self.club = Club.objects.get(name='KCL-Chess-Society')
        self.url = reverse('tournament_list', kwargs={'club_pk': self.club.pk})
        UserInClub.objects.create(
            user=self.user,
            user_level=3,
            club=self.club
        )

    def test_club_list_url(self):
        self.assertEqual(self.url,f'/club/{self.club.pk}/tournaments/')

    def test_get_club_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_tournament_list(self):
        self.client.login(username=self.user.email, password='Password123')
        self._create_test_Tournaments(15)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tournament_list.html')
        for i in range(15):
            tournament = Tournament.objects.get(name=f'Tournament{i}')
            tournament_url = reverse('show_tournament', kwargs={'club_pk': self.club.pk,'tournament_pk':tournament.pk})
            self.assertContains(response, tournament_url)


    def _create_test_Tournaments(self, club_count):
        for i in range(club_count):
            tournament = Tournament.objects.create(
                name=f'Tournament{i}',
                deadline='2022-12-23',
                description=f'Description{i}',
                finished=False,
                max_players=56,
                organiser=self.user,
                club=self.club
            )

            UserInTournament.objects.create(
                user=self.user,
                tournament=tournament,
                is_organiser=True,
                is_co_organiser=False
            )