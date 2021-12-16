import datetime

from django.test import TestCase
from django.urls import reverse
from chessManagement.forms import createClubForm, createTournamentForm
from chessManagement.models import User, Club, Tournament, UserInClub, UserInTournament, Game
from chessManagement.tests.helpers import reverse_with_next


class DecideGameOutcomeTestCase(TestCase):


    fixtures = [
        'chessManagement/tests/fixtures/default_user.json',
        'chessManagement/tests/fixtures/other_users.json',
        'chessManagement/tests/fixtures/default_club.json',
        'chessManagement/tests/fixtures/other_clubs.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.member_user = User.objects.get(username='janedoe@example.org')
        self.other_member = User.objects.get(username='peterpickles@example.org')
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
        UserInClub.objects.create(
            user=self.other_member,
            user_level=1,
            club=self.club
        )
        self.game = Game.objects.create(
            player1 = self.member_user,
            player2 = self.other_member,
            tournament = self.tournament,
            finished = False,
        )
        self.url = reverse('decide_game_outcome', kwargs={'club_pk': self.club.pk,'tournament_pk':self.tournament.pk,'game_pk': self.game.pk})

    def test_get_decide_game_outcome_url(self):
        self.assertEqual(self.url,f'/club/{self.club.pk}/tournament/{self.tournament.pk}/match/{self.game.pk}')

    def test_get_decide_game_outcome(self):
        self.client.login(username='johndoe@example.org', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'decide_game_outcome.html')

    def test_cannot_be_accessed_by_member(self):
        self.client.login(username=self.member_user.email, password='Password123')
        redirect_url = reverse('show_matches', kwargs={'club_pk': self.club.pk,'tournament_pk':self.tournament.pk})
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_succesful_entering_outcome(self):
        self.client.login(username='johndoe@example.org', password='Password123')
        form_input = { 'winner': "1" }
        response = self.client.post(self.url, form_input, follow=True)
        game = Game.objects.get(pk=self.game.pk)
        self.assertEqual(game.winner, "1")
        self.assertTrue(game.isFinished())
        redirect_url = reverse('show_matches', kwargs={'club_pk': self.club.pk,'tournament_pk':self.tournament.pk})
        self.assertRedirects(response, redirect_url)
