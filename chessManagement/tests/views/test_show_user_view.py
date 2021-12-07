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
        self.user = User.objects.get(username='johndoe@example.org')
        self.target_user = User.objects.get(username='janedoe@example.org')
        self.user_not_in_club = User.objects.get(username='peterpickles@example.org')
        self.officer_user = User.objects.get(username='petrapickles@example.org')
        self.applicant_user = User.objects.get(username='charliec@example.org')
        self.club = Club.objects.get(name='KCL-Chess-Society')


        """This should probably be in a fixture, but it works for now."""
        user_in_club = UserInClub.objects.create(
            user=self.user,
            club=self.club,
            user_level=3
        )

        applicant_user_in_club = UserInClub.objects.create(
            user=self.applicant_user,
            club=self.club,
            user_level=0
        )

        target_user_in_club = UserInClub.objects.create(
            user=self.target_user,
            club=self.club,
            user_level=1
        )

        officer_user_in_club = UserInClub.objects.create(
            user=self.officer_user,
            club=self.club,
            user_level=2
        )

        self.url = reverse('show_user', kwargs={'club_pk': self.club.pk, 'user_id': self.target_user.id})

    def test_show_user_url(self):
        self.assertEqual(self.url,f'/club/{self.club.pk}/user/{self.target_user.id}/')

    def test_get_show_user_which_is_not_in_the_club_and_with_valid_id(self):
        self.client.login(username=self.user_not_in_club.email, password='Password123')
        response = self.client.get(self.url, follow=True)
        response_url = reverse('club_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'club_list/all.html')

    def test_get_show_user_with_invalid_id(self):
        self.client.login(username=self.user.email, password='Password123')
        url = reverse('show_user', kwargs={'club_pk': self.club.pk, 'user_id': self.user.id+9999})
        response = self.client.get(url, follow=True)
        response_url = reverse('club_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'club_list/all.html')

    def test_get_show_user_with_own_id(self):
        self.client.login(username=self.user.email, password='Password123')
        url = reverse('show_user', kwargs={'club_pk': self.club.pk, 'user_id': self.user.id})
        response = self.client.get(url, follow=True)
        response_url = reverse('profile')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_owner_get_show_user_which_is_in_the_club_and_with_valid_id(self):
        self.client.login(username=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_member/for_owner.html')
        self.assertContains(response, "Jane Doe")
        self.assertContains(response, "janedoe@example.org")

    # def test_officer_get_show_user_which_is_in_the_club_and_with_valid_id(self):
    #     self.client.login(username=self.officer_user.email, password='Password123')
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'show_member/for_officer.html')
    #     self.assertContains(response, "Jane Doe")
    #     self.assertContains(response, "janedoe@example.org")

    def test_member_get_show_user_which_is_in_the_club_and_with_valid_id(self):
        self.client.login(username=self.target_user.email, password='Password123')
        url = reverse('show_user', kwargs={'club_pk': self.club.pk, 'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_member/for_member.html')
        self.assertContains(response, "John Doe")
        self.assertContains(response, "johndoe@example.org")

    def test_applicant_get_show_user_which_is_in_the_club_and_with_valid_id(self):
        self.client.login(username=self.applicant_user.email, password='Password123')
        response = self.client.get(self.url, follow=True)
        response_url = reverse('show_club', kwargs={'club_pk': self.club.pk})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'show_club/for_applicant.html')

    def test_get_show_user_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
