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
        self.member_user = User.objects.get(username='johndoe@example.org')
        self.owner_user = User.objects.get(username='janedoe@example.org')
        self.club = Club.objects.get(name='KCL-Chess-Society')


        """This should probably be in a fixture, but it works for now."""
        UserInClub.objects.create(
            user=self.member_user,
            club=self.club,
            user_level=1
        )

        UserInClub.objects.create(
            user=self.owner_user,
            club=self.club,
            user_level=3
        )

    def test_change_member_user_to_officer_by_owner(self):
        user = self.member_user
        self.client.login(username=self.owner_user.email, password='Password123')
        self.assertEqual(self.club.numberOfMembers(),2)
        url = reverse('to_officer', kwargs={'club_pk': self.club.pk, 'user_id': user.id})
        self.assertEqual(url,f'/club/{self.club.pk}/user/{user.id}/to_officer/')
        response = self.client.post(url, follow=True)
        response_url = reverse('show_user', kwargs={'club_pk': self.club.pk, 'user_id': user.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'show_member/for_owner.html')
        self.assertEqual(self.club.numberOfMembers(),2)
        self.assertFalse(user.isMemberOf(self.club))
        self.assertTrue(user.isOfficerOf(self.club))
