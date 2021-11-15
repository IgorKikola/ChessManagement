from django.test import TestCase
from django.urls import reverse
from chessManagement.models import User

class ShowUserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='John',
            first_name='John',
            last_name='Doe',
            email='johndoe@example.org',
            password='Password123',
            bio='The quick brown fox jumps over the lazy dog.',
            experience='Experience',
            personal_statement='Personal statement'
        )
        self.url = reverse('show_user', kwargs={'user_id': self.user.id})

    def test_show_user_url(self):
        self.assertEqual(self.url,f'/user/{self.user.id}')

    def test_get_show_user_with_valid_id(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_user.html')
        self.assertContains(response, "John Doe")
        self.assertContains(response, "John")

    def test_get_show_user_with_invalid_id(self):
        self.client.login(self.user.username=='johndoe@example.org', password='Password123')        
        url = reverse('show_user', kwargs={'user_id': self.user.id+1})
        response = self.client.get(url, follow=True)
        response_url = reverse('user_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'user_list.html')
