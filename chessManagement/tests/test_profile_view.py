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
        self.url = reverse('profile', kwargs={'user_id': self.user.id})

    def test_profile_url(self):
        self.assertEqual(self.url,f'/profile/{self.user.id}')

    def test_get_profile_with_valid_id(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertContains(response, "John Doe")
        self.assertContains(response, "johndoe@example.org")

    # def test_get_profile_with_invalid_id(self):
    #     url = reverse('profile', kwargs={'user_id': self.user.id+1})
    #     response = self.client.get(url, follow=True)
    #     response_url = reverse('user_list')
    #     self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
    #     self.assertTemplateUsed(response, 'user_list.html')
