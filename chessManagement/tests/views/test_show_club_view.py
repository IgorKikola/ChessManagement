from django.test import TestCase
from django.urls import reverse
from chessManagement.models import User, Club, UserInClub
from chessManagement.tests.helpers import reverse_with_next

class ShowUserTest(TestCase):

    fixtures = [
        'chessManagement/tests/fixtures/default_user.json',
        'chessManagement/tests/fixtures/other_users.json',
        'chessManagement/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.applicant_user = User.objects.get(username='johndoe@example.org')
        self.member_user = User.objects.get(username='janedoe@example.org')
        self.officer_user = User.objects.get(username='peterpickles@example.org')
        self.owner_user = User.objects.get(username='petrapickles@example.org')
        self.user_not_in_club = User.objects.get(username='charliec@example.org')
        self.club = Club.objects.get(name='KCL-Chess-Society')


        """This should probably be in a fixture, but it works for now."""
        user_in_club = UserInClub.objects.create(
            user=self.applicant_user,
            club=self.club,
            user_level=0
        )

        applicant_user_in_club = UserInClub.objects.create(
            user=self.member_user,
            club=self.club,
            user_level=1
        )

        target_user_in_club = UserInClub.objects.create(
            user=self.officer_user,
            club=self.club,
            user_level=2
        )

        officer_user_in_club = UserInClub.objects.create(
            user=self.owner_user,
            club=self.club,
            user_level=3
        )

        self.url = reverse('show_club', kwargs={'club_pk': self.club.pk})

    def test_show_user_url(self):
        self.assertEqual(self.url,f'/club/{self.club.pk}/')

    def test_get_show_club_by_user_is_not_in_the_club(self):
        self.client.login(username=self.user_not_in_club.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_club/for_applicant.html',)
        self.assertContains(response, "KCL-Chess-Society")

    def test_get_show_club_by_applicant_user(self):
        self.client.login(username=self.applicant_user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_club/for_applicant.html',)
        self.assertContains(response, "KCL-Chess-Society")

    def test_get_show_club_by_member_user(self):
        self.client.login(username=self.member_user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_club/for_member.html',)
        self.assertContains(response, "KCL-Chess-Society")

    def test_get_show_club_by_officer_user(self):
        self.client.login(username=self.officer_user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_club/for_officer.html',)
        self.assertContains(response, "KCL-Chess-Society")

    def test_get_show_club_by_owner_user(self):
        self.client.login(username=self.owner_user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_club/for_owner.html',)
        self.assertContains(response, "KCL-Chess-Society")


    def test_get_show_user_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
