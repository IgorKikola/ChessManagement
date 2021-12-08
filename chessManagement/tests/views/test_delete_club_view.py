from django.test import TestCase
from django.urls import reverse
from chessManagement.models import User, Club, UserInClub
from chessManagement.tests.helpers import reverse_with_next

class ToMemberTest(TestCase):

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
        UserInClub.objects.create(
            user=self.applicant_user,
            club=self.club,
            user_level=0
        )

        UserInClub.objects.create(
            user=self.member_user,
            club=self.club,
            user_level=1
        )

        UserInClub.objects.create(
            user=self.officer_user,
            club=self.club,
            user_level=2
        )

        UserInClub.objects.create(
            user=self.owner_user,
            club=self.club,
            user_level=3
        )

    def test_owner_user_can_delete_club(self):
        self.client.login(username=self.owner_user.email, password='Password123')
        url = reverse('delete_club', kwargs={'club_pk': self.club.pk})
        self.assertEqual(url,f'/club/{self.club.pk}/delete/')
        response = self.client.post(url, follow=True)
        response_url = reverse('club_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'club_list/all.html')
        self.assertNotContains(response, "KCL-Chess-Society")

    def test_user_not_in_club_cannot_delete_club(self):
        self.client.login(username=self.user_not_in_club.email, password='Password123')
        url = reverse('delete_club', kwargs={'club_pk': self.club.pk})
        self.assertEqual(url,f'/club/{self.club.pk}/delete/')
        response = self.client.post(url, follow=True)
        response_url = reverse('show_club', kwargs={'club_pk': self.club.pk})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'show_club/for_applicant.html')
        self.assertContains(response, "KCL-Chess-Society")

    def test_applicant_user_cannot_delete_club(self):
        self.client.login(username=self.applicant_user.email, password='Password123')
        url = reverse('delete_club', kwargs={'club_pk': self.club.pk})
        self.assertEqual(url,f'/club/{self.club.pk}/delete/')
        response = self.client.post(url, follow=True)
        response_url = reverse('show_club', kwargs={'club_pk': self.club.pk})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'show_club/for_applicant.html')
        self.assertContains(response, "KCL-Chess-Society")

    def test_member_user_cannot_delete_club(self):
        self.client.login(username=self.member_user.email, password='Password123')
        url = reverse('delete_club', kwargs={'club_pk': self.club.pk})
        self.assertEqual(url,f'/club/{self.club.pk}/delete/')
        response = self.client.post(url, follow=True)
        response_url = reverse('show_club', kwargs={'club_pk': self.club.pk})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'show_club/for_member.html')
        self.assertContains(response, "KCL-Chess-Society")

    def test_officer_user_cannot_delete_club(self):
        self.client.login(username=self.officer_user.email, password='Password123')
        url = reverse('delete_club', kwargs={'club_pk': self.club.pk})
        self.assertEqual(url,f'/club/{self.club.pk}/delete/')
        response = self.client.post(url, follow=True)
        response_url = reverse('show_club', kwargs={'club_pk': self.club.pk})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'show_club/for_officer.html')
        self.assertContains(response, "KCL-Chess-Society")
