"""Tests of the sign up view."""
import datetime

from django.test import TestCase
from django.urls import reverse
from chessManagement.forms import createClubForm, createTournamentForm
from chessManagement.models import User, Club, Tournament


class CreateTournamentViewTestCase(TestCase):
    """Tests of the create club view."""

    fixtures = [
        'chessManagement/tests/fixtures/default_user.json',
        'chessManagement/tests/fixtures/other_users.json',
        'chessManagement/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.club = Club.objects.get(name='KCL-Chess-Society')
        self.form_input = {
            'name':'My Tournament',
            'deadline':'2022-11-23',
            'max_players': 56,
            'description':'The official KCL Chess Society tournament.'
        }
        self.url = reverse('create_tournament', kwargs={'club_pk': self.club.pk})

    def test_get_create_tournament_url(self):
        self.assertEqual(self.url,f'/create_tournament/{self.club.pk}/')

    def test_get_create_tournament(self):
        self.client.login(username='johndoe@example.org', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_tournament.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, createTournamentForm))
        self.assertFalse(form.is_bound)

    def test_unsuccesful_create(self):
        self.client.login(username='johndoe@example.org', password='Password123')
        self.form_input['name'] = ''
        before_count = Tournament.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Tournament.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_tournament.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, createTournamentForm))
        self.assertTrue(form.is_bound)

    def test_successful_create(self):
        self.client.login(username='johndoe@example.org', password='Password123')
        before_count = Tournament.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Tournament.objects.count()
        self.assertEqual(after_count, before_count+1)
        tournament = Tournament.objects.get(name='My Tournament')
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(tournament.name, 'My Tournament')
        self.assertEqual(tournament.description, 'The official KCL Chess Society tournament.')
        self.assertEqual(tournament.deadline,datetime.date(2022, 11, 23))
        self.assertEqual(tournament.max_players, 56)
