from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import authenticate,login
from chessManagement.models import User
from chessManagement.tests.helpers import reverse_with_next

class UserListTest(TestCase):

    fixtures = ['chessManagement/tests/fixtures/other_users.json']

    def setUp(self):
        self.url = reverse('user_list')
        self.user = User.objects.get(email='janedoe@example.org')

    def test_user_list_url(self):
        self.assertEqual(self.url,'/users/')

    def test_get_user_list(self):
        self.client.login(username=self.user.email, password='Password123')
        self._create_test_users(15-1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list.html')
        self.assertEqual(len(response.context['users']), 15)
        for user_id in range(15-1):
            self.assertContains(response, f'First{user_id}')
            self.assertContains(response, f'Last{user_id}')
            user = User.objects.get(username=f'user{user_id}@example.org')
            user_url = reverse('show_user', kwargs={'user_id': user.id})
            self.assertContains(response, user_url)

    # def test_get_user_list_redirects_when_not_logged_in(self):
    #     redirect_url = reverse_with_next('log_in', self.url)
    #     response = self.client.get(self.url)
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def _create_test_users(self, user_count):
        for user_id in range(user_count):
            User.objects.create_user(
                user_level=0,
                email=f'user{user_id}@example.org',
                username=f'user{user_id}@example.org',
                password='Password123',
                first_name=f'First{user_id}',
                last_name=f'Last{user_id}',
                bio=f'Bio {user_id}',
                experience=f'Experience {user_id}',
                personal_statement=f'Personal statement {user_id}',
            )
