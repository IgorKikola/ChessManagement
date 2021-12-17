import datetime

from django.test import TestCase
from django.urls import reverse
from chessManagement.forms import createClubForm, createTournamentForm
from chessManagement.models import User, Club, Tournament, UserInClub, UserInTournament
from chessManagement.tests.helpers import reverse_with_next


class ShowMatchesViewTestCase(TestCase):


    fixtures = [
        'chessManagement/tests/fixtures/default_user.json',
        'chessManagement/tests/fixtures/other_users.json',
        'chessManagement/tests/fixtures/default_club.json',
        'chessManagement/tests/fixtures/other_clubs.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.member_user = User.objects.get(username='janedoe@example.org')
        self.club = Club.objects.get(name='KCL-Chess-Society')
        self.tournament = Tournament.objects.create(
            name="John Tournament",
            club=self.club,
            description="this is johns tournament",
            organiser=self.user,
            max_players=56,
            deadline='2069-12-27',
            finished=False
        )
        UserInTournament.objects.create(
            user=self.user,
            tournament=self.tournament,
            is_organiser=True,
            is_co_organiser=False
        )
        UserInClub.objects.create(
            user=self.user,
            user_level=3,
            club=self.club
        )
        UserInClub.objects.create(
            user=self.member_user,
            user_level=1,
            club=self.club
        )
        self.url = reverse('show_matches', kwargs={'club_pk': self.club.pk,'tournament_pk':self.tournament.pk})

    def test_get_show_matches_url(self):
        self.assertEqual(self.url,f'/club/{self.club.pk}/tournament/{self.tournament.pk}/matches/')

    def test_get_show_matches(self):
        self.client.login(username='johndoe@example.org', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_scheduled_matches/for_organisers.html')

    def test_get_show_matches_by_member_user(self):
        self.client.login(username=self.member_user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_scheduled_matches/for_members.html')

    def test_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
