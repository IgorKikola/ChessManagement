from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import authenticate,login
from chessManagement.models import User, Club
from chessManagement.tests.helpers import reverse_with_next
from chessManagement.forms import createClubForm

class ClubListTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username = 'janedoe@example.org',
            first_name='Jane',
            last_name='Doe',
            email='janedoe@example.org',
            experience='Beginner',
            personal_statement='Hi I would like to apply ',
            bio='Hello, I am Jane Doe.',
            password='Password123',
        )
        self.url = reverse('club_list')

    def test_club_list_url(self):
        self.assertEqual(self.url,'/clubs/')

    def test_get_user_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_club_list(self):
        self.client.login(username=self.user.email, password='Password123')
        self._create_test_clubs(15)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_list.html')
        self.assertEqual(len(response.context['clubs']), 15)
        for i in range(15):
            club = Club.objects.get(name=f'Club{i}')
            club_url = reverse('show_club_and_user_list', kwargs={'pk': club.pk})
            self.assertContains(response, club_url)

    def _create_test_clubs(self, club_count):
        for i in range(club_count):
            form_input = {
                'name':f'Club{i}',
                'location':f'Location{i}',
                'description':f'Description{i}',
            }

            form = createClubForm(data=form_input)
            form.save(self.user)
