"""Tests of the apply club view."""
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from chessManagement.models import User, Club, UserInClub
from chessManagement.tests.helpers import reverse_with_next

class ApplyClubViewTestCase(TestCase):
    """Tests of the apply club view."""

    fixtures = [
        'chessManagement/tests/fixtures/default_user.json',
        'chessManagement/tests/fixtures/other_users.json',
        'chessManagement/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.owner_user = User.objects.get(username='janedoe@example.org')
        self.club = Club.objects.get(name='KCL-Chess-Society')

        owner_user_in_club = UserInClub.objects.create(
            user=self.owner_user,
            club=self.club,
            user_level=3
        )

        self.url = reverse('apply_Club', kwargs={'club_pk': self.club.pk})

    def test_apply_club_url(self):
        self.assertEqual(self.url, f'/club/{self.club.pk}/apply/')

    def test_get_apply_club_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_succesful_apply_to(self):
        self.client.login(username='johndoe@example.org', password='Password123')
        before_count = len(UserInClub.objects.filter(club=self.club, user=self.user))
        response = self.client.post(self.url, follow=True)
        response_url = reverse('show_club', kwargs={'club_pk': self.club.pk})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        after_count = len(UserInClub.objects.filter(club=self.club, user=self.user))
        self.assertEqual(after_count, before_count+1)
        self.assertTemplateUsed(response, 'show_club/for_applicant.html')
        club = Club.objects.get(pk=self.club.pk)
        self.assertTrue(club.name == "KCL-Chess-Society")

    def test_already_apply_to(self):
        self.client.login(username='johndoe@example.org', password='Password123')
        UserInClub.objects.create(
            user=self.user,
            club=self.club,
            user_level=0
        )
        before_count = len(UserInClub.objects.filter(club=self.club, user=self.user))
        response = self.client.post(self.url, follow=True)
        response_url = reverse('show_club', kwargs={'club_pk': self.club.pk})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'show_club/for_applicant.html')
        after_count = len(UserInClub.objects.filter(club=self.club, user=self.user))
        self.assertEqual(after_count, before_count)
        club = Club.objects.get(pk=self.club.pk)
        self.assertTrue(club.name == "KCL-Chess-Society")
