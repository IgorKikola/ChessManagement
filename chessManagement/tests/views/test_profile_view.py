from django.test import TestCase
from django.urls import reverse
from chessManagement.models import User
from chessManagement.tests.helpers import reverse_with_next

class ProfileTest(TestCase):

    fixtures = ['chessManagement/tests/fixtures/default_user.json']

    def setUp(self):

        self.user = User.objects.get(username='johndoe@example.org')
        self.url = reverse('profile')

    def test_profile_url(self):
        self.assertEqual(self.url,'/profile/')

    def test_get_profile_with_valid_id(self):
        self.client.login(username='johndoe@example.org', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertContains(response, "John Doe")
        self.assertContains(response, "johndoe@example.org")

    def test_get_profile_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
