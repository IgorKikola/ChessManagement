import datetime

from django.test import TestCase
from django.urls import reverse
from chessManagement.forms import createClubForm, createTournamentForm
from chessManagement.models import User, Club, Tournament, UserInClub, UserInTournament, Game, Stage, Group
from chessManagement.tests.helpers import reverse_with_next


class NextStageTestCase(TestCase):


    fixtures = [
        'chessManagement/tests/fixtures/default_user.json',
        'chessManagement/tests/fixtures/other_users.json',
        'chessManagement/tests/fixtures/default_club.json',
        'chessManagement/tests/fixtures/other_clubs.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.officer_user = User.objects.get(username='janedoe@example.org')
        self.club = Club.objects.get(name='KCL-Chess-Society')
        self.tournament = Tournament.objects.create(
            name="John Tournament",
            club=self.club,
            description="this is johns tournament",
            organiser=self.user,
            max_players=56,
            deadline='1984-01-01',
            finished=False
        )
        UserInClub.objects.create(
            user=self.user,
            user_level=3,
            club=self.club
        )
        UserInClub.objects.create(
            user=self.officer_user,
            user_level=2,
            club=self.club
        )
        UserInTournament.objects.create(
            user=self.officer_user,
            tournament=self.tournament,
            is_organiser=False,
            is_co_organiser=True
        )
        UserInTournament.objects.create(
            user=self.user,
            tournament=self.tournament,
            is_organiser=True,
            is_co_organiser=False
        )
        self.url = reverse('schedule_matches', kwargs={'club_pk': self.club.pk,'tournament_pk':self.tournament.pk})

    def test_get_next_stage_url(self):
        self.assertEqual(self.url,f'/club/{self.club.pk}/tournament/{self.tournament.pk}/matches/schedule/')

    def test_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_non_organiser_cannot_schedule(self):
        self._create_test_users(2)
        self.client.login(username='user1@test.org', password='Password123')
        redirect_url = reverse('show_matches', kwargs={'club_pk': self.club.pk,'tournament_pk':self.tournament.pk})
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        tournament = Tournament.objects.get(pk=self.tournament.pk)
        self.assertEquals(tournament.current_stage, None)

    def test_organiser_can_schedule(self):
        self.client.login(username=self.user.username, password='Password123')
        self._create_test_users(2)
        redirect_url = reverse('show_matches', kwargs={'club_pk': self.club.pk,'tournament_pk':self.tournament.pk})
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url)
        tournament = Tournament.objects.get(pk=self.tournament.pk)
        self.assertTrue(tournament.current_stage != None)

    def test_co_organiser_can_schedule(self):
        self.client.login(username=self.officer_user.username, password='Password123')
        self._create_test_users(2)
        redirect_url = reverse('show_matches', kwargs={'club_pk': self.club.pk,'tournament_pk':self.tournament.pk})
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url)
        tournament = Tournament.objects.get(pk=self.tournament.pk)
        self.assertTrue(tournament.current_stage != None)

    def test_cannot_schedule_after_finals(self):
        self.client.login(username=self.user.username, password='Password123')
        self._create_test_users(2)
        self.client.get(self.url)
        tournament = Tournament.objects.get(pk=self.tournament.pk)
        stage = tournament.current_stage
        self.assertTrue(stage != None)
        self.client.get(self.url)
        self.assertEqual(stage, tournament.current_stage)

    def test_can_schedule_after_semifinals(self):
        self.client.login(username=self.user.username, password='Password123')
        self._create_test_users(4)
        self.client.get(self.url)
        tournament = Tournament.objects.get(pk=self.tournament.pk)
        stage = tournament.current_stage
        self.assertTrue(stage != None)
        self.assertFalse(stage.gamesAreFinished())
        self._set_game_winners(stage)
        self.assertTrue(stage.gamesAreFinished())
        self.client.get(self.url)
        tournament = Tournament.objects.get(pk=self.tournament.pk)
        self.assertFalse(stage == tournament.current_stage)

    def test_semifinals_are_single_elimination_type_stage(self):
        self.client.login(username=self.user.username, password='Password123')
        self._create_test_users(4)
        self.client.get(self.url)
        tournament = Tournament.objects.get(pk=self.tournament.pk)
        stage = tournament.current_stage
        self.assertFalse(stage.typeIsElimination())

    def test_five_person_group_stage_is_group_type_stage(self):
        self.client.login(username=self.user.username, password='Password123')
        self._create_test_users(5)
        self.client.get(self.url)
        tournament = Tournament.objects.get(pk=self.tournament.pk)
        stage = tournament.current_stage
        self.assertTrue(stage.typeIsElimination())

    def test_twenty_person_group_stage_is_group_type_stage(self):
        self.client.login(username=self.user.username, password='Password123')
        self._create_test_users(20)
        self.client.get(self.url)
        tournament = Tournament.objects.get(pk=self.tournament.pk)
        stage = tournament.current_stage
        self.assertTrue(stage.typeIsElimination())

    def test_tournament_with_group_stages(self):
        self.client.login(username=self.user.username, password='Password123')
        self._create_test_users(96)
        self.client.get(self.url)
        tournament = Tournament.objects.get(pk=self.tournament.pk)
        self.assertTrue(len(tournament.current_stage.players()) == 96)
        self._set_game_winners(tournament.current_stage)
        self.client.get(self.url)
        tournament = Tournament.objects.get(pk=self.tournament.pk)
        self.assertTrue(len(tournament.current_stage.players()) == 32)
        self._set_game_winners(tournament.current_stage)
        self.client.get(self.url)
        tournament = Tournament.objects.get(pk=self.tournament.pk)
        self.assertTrue(len(tournament.current_stage.players()) == 16)
        self._set_game_winners(tournament.current_stage)
        self.client.get(self.url)
        tournament = Tournament.objects.get(pk=self.tournament.pk)
        self.assertTrue(len(tournament.current_stage.players()) == 8)
        self._set_game_winners(tournament.current_stage)
        self.client.get(self.url)
        tournament = Tournament.objects.get(pk=self.tournament.pk)
        self.assertTrue(len(tournament.current_stage.players()) == 4)
        self._set_game_winners(tournament.current_stage)
        self.client.get(self.url)
        tournament = Tournament.objects.get(pk=self.tournament.pk)
        self.assertTrue(len(tournament.current_stage.players()) == 2)

    def test_players_from_same_group_are_separated(self):
        self.client.login(username=self.user.username, password='Password123')
        self._create_test_users(7)
        self.client.get(self.url)
        tournament = Tournament.objects.get(pk=self.tournament.pk)
        self._set_game_winners(tournament.current_stage)
        tournament = Tournament.objects.get(pk=self.tournament.pk)
        group = tournament.current_stage.groups().first()
        user1 = User.objects.get(username='user1@test.org')
        user2 = User.objects.get(username='user2@test.org')
        self.assertEqual(group.winners(), [user1, user2])
        self.client.get(self.url)
        tournament = Tournament.objects.get(pk=self.tournament.pk)
        group = tournament.current_stage.groups().first()
        self.assertTrue(group.players()[0] == user1)
        self.assertFalse(group.players()[1] == user2)


    def _set_game_winners(self, stage):
        groups = stage.groups()
        for group in groups:
            if stage.typeIsElimination():
                winners = [group.players().first(), group.players()[1]]
            else:
                winners = [group.players()[0]]
            for game in group.games():
                if game.getPlayer1() in winners:
                    game.setWinner("1")
                elif game.getPlayer2() in winners:
                    game.setWinner("2")
                else:
                    game.setWinner("0")
                game.setFinished()
                game.save()

    def _create_test_users(self, user_count):
        for user_id in range(1, user_count+1):
            user = User.objects.create_user(
                email=f'user{user_id}@test.org',
                username=f'user{user_id}@test.org',
                password='Password123',
                first_name=f'First{user_id}',
                last_name=f'Last{user_id}',
                bio=f'Bio {user_id}',
                experience="Beginner",
                personal_statement="statement"
            )

            UserInClub.objects.create(
                user=user,
                club=self.club,
                user_level=1
            )

            UserInTournament.objects.create(
                user = user,
                tournament = self.tournament,
                is_organiser = False,
                is_co_organiser = False,
            )
