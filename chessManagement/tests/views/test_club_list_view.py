from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import authenticate,login
from chessManagement.models import User, Club, UserInClub
from chessManagement.tests.helpers import reverse_with_next
from chessManagement.forms import createClubForm

class ClubListTest(TestCase):

    fixtures = [
        'chessManagement/tests/fixtures/default_user.json',
        'chessManagement/tests/fixtures/other_users.json'
    ]


    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.other_owner_user = User.objects.get(username='janedoe@example.org')
        self.url = reverse('club_list')

    def test_club_list_url(self):
        self.assertEqual(self.url,'/clubs/')

    def test_get_club_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_club_list(self):
        self.client.login(username=self.user.email, password='Password123')
        self._create_test_clubs(15)
        self._create_test_clubs_for_other_owner_user(15)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_list/all.html')
        self.assertEqual(len(response.context['clubs']), 30)
        for i in range(15):
            club = Club.objects.get(name=f'Club{i}')
            club_url = reverse('show_club', kwargs={'club_pk': club.pk})
            self.assertContains(response, club_url)

            clubForOther = Club.objects.get(name=f'ClubForOther{i}')
            clubForOther_url = reverse('show_club', kwargs={'club_pk': clubForOther.pk})
            self.assertContains(response, clubForOther_url)

    def _create_test_clubs(self, club_count):
        for i in range(club_count):
            club = Club.objects.create(
                name=f'Club{i}',
                location=f'Location{i}',
                description=f'Description{i}'
            )

            UserInClub.objects.create(
                user=self.user,
                club=club,
                user_level=3
            )

    def _create_test_clubs_for_other_owner_user(self, club_count):
        for i in range(club_count):
            club = Club.objects.create(
                name=f'ClubForOther{i}',
                location=f'LocationForOther{i}',
                description=f'DescriptionForOther{i}'
            )

            UserInClub.objects.create(
                user=self.other_owner_user,
                club=club,
                user_level=3
            )
