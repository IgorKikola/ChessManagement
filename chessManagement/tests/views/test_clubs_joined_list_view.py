from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import authenticate,login
from chessManagement.models import User, Club, UserInClub
from chessManagement.tests.helpers import reverse_with_next
from chessManagement.forms import createClubForm

class clubsAppliedToListTest(TestCase):

    fixtures = [
        'chessManagement/tests/fixtures/default_user.json',
        'chessManagement/tests/fixtures/other_users.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.owner_user = User.objects.get(username='janedoe@example.org')
        self.url = reverse('clubs_joined_list')

    def test_club_list_url(self):
        self.assertEqual(self.url,'/clubs/joined/')

    def test_get_club_joined_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_clubs_applied_to_list(self):
        self.client.login(username=self.user.email, password='Password123')
        self._create_test_clubs(15)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_list/joined.html')
        self.assertEqual(len(response.context['clubs']), 30)
        for i in range(30):
            club = Club.objects.get(name=f'Club{i}')
            club_url = reverse('show_club', kwargs={'club_pk': club.pk})
            self.assertContains(response, club_url)

    def _create_test_clubs(self, club_count):
        for i in range(club_count):
            club = Club.objects.create(
                name=f'Club{i}',
                location=f'Location{i}',
                description=f'Description{i}'
            )

            UserInClub.objects.create(
                user=self.owner_user,
                club=club,
                user_level=3
            )

            UserInClub.objects.create(
                user=self.user,
                club=club,
                user_level=1
            )

        for i+club_count in range(club_count):
            club = Club.objects.create(
                name=f'Club{i+club_count}',
                location=f'Location{i+club_count}',
                description=f'Description{i+club_count}'
            )

            UserInClub.objects.create(
                user=self.owner_user,
                club=club,
                user_level=3
            )

            UserInClub.objects.create(
                user=self.user,
                club=club,
                user_level=2
            )
