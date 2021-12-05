from django.test import TestCase
from django.urls import reverse
from chessManagement.models import User

class ShowUserTest(TestCase):

    fixtures = [
        'chessManagement/tests/fixtures/default_user.json',
        'chessManagement/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.target_user = User.objects.get(username='janedoe@example.org')
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
