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

    def test_change_applicant_user_to_member_by_owner(self):
        user = self.applicant_user
        self.client.login(username=self.owner_user.email, password='Password123')
        self.assertEqual(self.club.numberOfMembers(),3)
        url = reverse('to_member', kwargs={'club_pk': self.club.pk, 'user_id': user.id})
        self.assertEqual(url,f'/club/{self.club.pk}/user/{user.id}/to_member/')
        response = self.client.post(url, follow=True)
        response_url = reverse('applicants', kwargs={'club_pk': self.club.pk})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'applicant_list.html')
        self.assertEqual(self.club.numberOfMembers(),4)
        self.assertTrue(user.isMemberOf(self.club))
        self.assertFalse(user.isApplicantIn(self.club))

    def test_change_applicant_user_to_member_by_officer(self):
        user = self.applicant_user
        self.client.login(username=self.officer_user.email, password='Password123')
        self.assertEqual(self.club.numberOfMembers(),3)
        url = reverse('to_member', kwargs={'club_pk': self.club.pk, 'user_id': user.id})
        self.assertEqual(url,f'/club/{self.club.pk}/user/{user.id}/to_member/')
        response = self.client.post(url, follow=True)
        response_url = reverse('applicants', kwargs={'club_pk': self.club.pk})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'applicant_list.html')
        self.assertEqual(self.club.numberOfMembers(),4)
        self.assertTrue(user.isMemberOf(self.club))
        self.assertFalse(user.isApplicantIn(self.club))

    def test_change_officer_user_to_member_by_owner(self):
        user = self.officer_user
        self.client.login(username=self.owner_user.email, password='Password123')
        self.assertEqual(self.club.numberOfMembers(),3)
        url = reverse('to_member', kwargs={'club_pk': self.club.pk, 'user_id': user.id})
        self.assertEqual(url,f'/club/{self.club.pk}/user/{user.id}/to_member/')
        response = self.client.post(url, follow=True)
        response_url = reverse('show_user', kwargs={'club_pk': self.club.pk, 'user_id': user.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'show_member/for_owner.html')
        self.assertEqual(self.club.numberOfMembers(),3)
        self.assertTrue(user.isMemberOf(self.club))
        self.assertFalse(user.isOfficerOf(self.club))

    # def test_cannot_change_officer_user_to_member_by_applicant(self):
    #     user = self.officer_user
    #     self.client.login(username=self.applicant_user.email, password='Password123')
    #     self.assertEqual(self.club.numberOfMembers(),3)
    #     url = reverse('to_member', kwargs={'club_pk': self.club.pk, 'user_id': user.id})
    #     self.assertEqual(url,f'/club/{self.club.pk}/user/{user.id}/to_member/')
    #     response = self.client.post(url, follow=True)
    #     response_url = reverse('show_club', kwargs={'club_pk': self.club.pk})
    #     self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
    #     self.assertTemplateUsed(response, 'show_club/for_applicant.html')
    #     self.assertEqual(self.club.numberOfMembers(),3)
    #     self.assertFalse(user.isMemberOf(self.club))
    #     self.assertTrue(user.isOfficerOf(self.club))
    #
    # def test_cannot_change_applicant_user_to_member_by_applicant(self):
    #     user = self.applicant_user
    #     self.client.login(username=self.applicant_user.email, password='Password123')
    #     self.assertEqual(self.club.numberOfMembers(),3)
    #     url = reverse('to_member', kwargs={'club_pk': self.club.pk, 'user_id': user.id})
    #     self.assertEqual(url,f'/club/{self.club.pk}/user/{user.id}/to_member/')
    #     response = self.client.post(url, follow=True)
    #     response_url = reverse('show_club', kwargs={'club_pk': self.club.pk})
    #     self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
    #     self.assertTemplateUsed(response, 'show_club/for_applicant.html')
    #     self.assertEqual(self.club.numberOfMembers(),3)
    #     self.assertFalse(user.isMemberOf(self.club))
    #     self.assertTrue(user.isApplicantIn(self.club))
