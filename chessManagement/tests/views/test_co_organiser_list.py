from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import authenticate,login
from chessManagement.models import User, Club, UserInClub, Tournament, UserInTournament
from chessManagement.tests.helpers import reverse_with_next
from chessManagement.forms import createClubForm

class CoOrganisersTestView(TestCase):

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
        self.url = reverse('co_organiser_list', kwargs={'tournament_pk': self.tournament.pk})


    def test_club_list_url(self):
        self.assertEqual(self.url,f'/tournament/co_organiser_list/{self.tournament.pk}/')

    def test_get_club_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_tournament_list(self):
        self.client.login(username=self.user.email, password='Password123')
        self._create_test_co_organisers(15)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tournament_users/co_organiser_list.html')
        for user_id in range(15):
            officer = User.objects.get(username=f'user{user_id}@test.org')
            tournament_url = reverse('show_user', kwargs={'club_pk': self.club.pk,'user_id':officer.pk})
            self.assertContains(response, tournament_url)


    def _create_test_co_organisers(self, user_count=10):
        for user_id in range(user_count):
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
                user_level=2
            )
            UserInTournament.objects.create(
                user=user,
                tournament=self.tournament,
                is_co_organiser=True,
                is_organiser=False
            )