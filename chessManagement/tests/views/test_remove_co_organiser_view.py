"""Tests of the sign up view."""

from django.test import TestCase
from django.urls import reverse
from chessManagement.models import User, Club, Tournament, UserInTournament, UserInClub


class SignUpTournamentViewTestCase(TestCase):
    """Tests of the create club view."""

    fixtures = [
        'chessManagement/tests/fixtures/default_user.json',
        'chessManagement/tests/fixtures/other_users.json',
        'chessManagement/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.other_owner_user = User.objects.get(username='janedoe@example.org')
        self.club = Club.objects.get(name='KCL-Chess-Society')
        self.tournament = Tournament.objects.create(
            name="John Tournament",
            club=self.club,
            description="this is johns tournament",
            organiser=self.user,
            max_players=56,
            deadline='2022-12-27',
            finished=False
        )
        UserInTournament.objects.create(
            user=self.user,
            tournament=self.tournament,
            is_organiser=True,
            is_co_organiser=False
        )
        UserInClub.objects.create(
            user=self.other_owner_user,
            user_level=1,
            club=self.club
        )
        UserInTournament.objects.create(
            user=self.other_owner_user,
            tournament=self.tournament,
            is_organiser=False,
            is_co_organiser=True
        )
        self.url = reverse('remove_co_organiser', kwargs={'tournament_pk': self.tournament.pk,'user_id':self.other_owner_user.pk,'club_pk': self.club.pk})

    def test_get_withdraw_tournament_url(self):
        self.assertEqual(self.url,f'/club/{self.club.pk}/tournament/{self.tournament.pk}/co-organisers/remove/{self.other_owner_user.pk}/')

    def test_successful_withdraw(self):
        self.client.login(username='johndoe@example.org', password='Password123')
        before_count = UserInTournament.objects.count()
        response = self.client.post(self.url,follow=True)
        after_count = UserInTournament.objects.count()
        self.assertTemplateUsed(response, 'co_organiser_list.html')
        self.assertEqual(after_count, before_count-1)