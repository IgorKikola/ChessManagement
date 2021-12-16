"""Tests of the sign up view."""
import datetime

from django.test import TestCase
from django.urls import reverse
from chessManagement.forms import createClubForm, createTournamentForm
from chessManagement.models import User, Club, Tournament, UserInClub, UserInTournament
from chessManagement.tests.helpers import reverse_with_next


class ShowTournamentViewTestCase(TestCase):
    """Tests of the create club view."""


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
            deadline='2021-12-27',
            finished=False
        )
        UserInTournament.objects.create(
            user=self.user,
            tournament=self.tournament,
            is_organiser=True,
            is_co_organiser=False
        )
        self.url = reverse('show_tournament', kwargs={'club_pk': self.club.pk,'tournament_pk':self.tournament.pk})

    def test_get_show_tournament_url(self):
        self.assertEqual(self.url,f'/club/{self.club.pk}/{self.tournament.pk}')

    def test_get_show_tournament(self):
        self.client.login(username='johndoe@example.org', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_tournament/for_organiser.html')
        self.assertContains(response, "John Tournament")
        self.assertContains(response, "johndoe@example.org")

    def test_get_show_tournament_by_member_user(self):
        self.client.login(username=self.member_user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_tournament/for_members.html',)
        self.assertContains(response, "John Tournament")
        self.assertContains(response, "johndoe@example.org")

    def test_get_show_user_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

