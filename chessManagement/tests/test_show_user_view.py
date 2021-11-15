from django.test import TestCase
from django.urls import reverse
from chessManagement.models import User

class ShowUserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='johndoe@example.org',
            experience = 'Beginner',
            personal_statement = 'Hi I would like to apply ',
            bio='Hello, I am John Doe.',
            password='Password123',
            is_active=True,
        )
        self.url = reverse('show_user', kwargs={'user_id': self.user.id})

    def test_show_user_url(self):
        self.assertEqual(self.url,f'/user/{self.user.id}')

    def test_get_show_user_with_valid_id(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_user.html')
        self.assertContains(response, "John Doe")


    def test_get_show_user_with_invalid_id(self):
        self.client.login(username=self.user.email, password='Password123')
        url = reverse('show_user', kwargs={'user_id': self.user.id+1})
        response = self.client.get(url, follow=True)
        response_url = reverse('user_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'user_list.html')
