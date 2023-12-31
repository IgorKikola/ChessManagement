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
        applicant_user_in_club = UserInClub.objects.create(
            user=self.applicant_user,
            club=self.club,
            user_level=0
        )

        member_user_in_club = UserInClub.objects.create(
            user=self.member_user,
            club=self.club,
            user_level=1
        )

        officer_user_in_club = UserInClub.objects.create(
            user=self.officer_user,
            club=self.club,
            user_level=2
        )

        owner_user_in_club = UserInClub.objects.create(
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
        self.assertContains(response, "janedoe@example.org")
        self.assertContains(response, "peterpickles@example.org")
        self.assertContains(response, "petrapickles@example.org")

    def test_get_show_club_by_applicant_user(self):
        self.client.login(username=self.applicant_user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_club/for_applicant.html',)
        self.assertContains(response, "KCL-Chess-Society")
        self.assertContains(response, "janedoe@example.org")
        self.assertContains(response, "peterpickles@example.org")
        self.assertContains(response, "petrapickles@example.org")

    def test_get_show_club_by_member_user(self):
        self.client.login(username=self.member_user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_club/for_member.html',)
        self.assertContains(response, "KCL-Chess-Society")
        self.assertContains(response, "janedoe@example.org")
        self.assertContains(response, "peterpickles@example.org")
        self.assertContains(response, "petrapickles@example.org")

    def test_get_show_club_by_officer_user(self):
        self.client.login(username=self.officer_user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_club/for_officer.html',)
        self.assertContains(response, "KCL-Chess-Society")
        self.assertContains(response, "janedoe@example.org")
        self.assertContains(response, "peterpickles@example.org")
        self.assertContains(response, "petrapickles@example.org")

    def test_get_show_club_by_owner_user(self):
        self.client.login(username=self.owner_user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_club/for_owner.html',)
        self.assertContains(response, "KCL-Chess-Society")
        self.assertEqual(self.club.numberOfMembers(), 3)
        self.assertContains(response, "janedoe@example.org")
        self.assertContains(response, "peterpickles@example.org")
        self.assertContains(response, "petrapickles@example.org")


    def test_get_show_user_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_user_list_in_this_club(self):
        self.client.login(username=self.owner_user.username, password='Password123')
        self._create_test_users(15-3)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_club/for_owner.html')
        self.assertEqual(self.club.numberOfMembers(), 15)
        for user_id in range(15-3):
            self.assertContains(response, f'user{user_id}@test.org')
            self.assertContains(response, f'First{user_id}')
            self.assertContains(response, f'Last{user_id}')
            user = User.objects.get(username=f'user{user_id}@test.org')
            user_url = reverse('show_user', kwargs={'club_pk': self.club.pk, 'user_id': user.id})
            self.assertContains(response, user_url)

    def _create_test_users(self, user_count=10):
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
                user_level=1
            )
