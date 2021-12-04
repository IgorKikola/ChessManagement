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
        self.target_user = User.objects.create_user(
            username = 'janedoe@example.org',
            first_name='Jane',
            last_name='Doe',
            email='janedoe@example.org',
            experience='Beginner',
            personal_statement='Hi I would like to apply ',
            bio='Hello, I am Jane Doe.',
            password='Password123',
        )
        self.url = reverse('show_user', kwargs={'user_id': self.target_user.id})

    def test_show_user_url(self):
        self.assertEqual(self.url,f'/user/{self.target_user.id}/')

    def test_get_show_user_which_is_not_in_the_club_and_with_valid_id(self):
        self.client.login(username=self.user.email, password='Password123')
        response = self.client.get(self.url, follow=True)
        response_url = reverse('club_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'club_list.html')

    def test_get_show_user_with_invalid_id(self):
        self.client.login(username=self.user.email, password='Password123')
        url = reverse('show_user', kwargs={'user_id': self.user.id+9999})
        response = self.client.get(url, follow=True)
        response_url = reverse('club_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'club_list.html')

    """Should write tests for test_get_show_user_with_own_id"""
    """Need to create Club and UserInClub in these tests"""
