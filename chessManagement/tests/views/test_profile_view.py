from django.test import TestCase
from django.urls import reverse
from chessManagement.models import User

class ProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='johndoe@example.org',
            experience='Beginner',
            personal_statement='Hi I would like to apply ',
            bio='Hello, I am John Doe.',
            password='Password123',
        )
        self.url = reverse('profile')
        self.client.login(username='johndoe@example.org', password='Password123')

    def test_profile_url(self):
        self.assertEqual(self.url,'/profile/')

    def test_get_profile_with_valid_id(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertContains(response, "John Doe")
        self.assertContains(response, "johndoe@example.org")





    """Shold write the tests for counting clubs and only show club that the user joins"""
