"""Tests of the sign up view."""
from django.test import TestCase
from django.urls import reverse
from chessManagement.forms import createClubForm
from chessManagement.models import User, Club

class CreateClubViewTestCase(TestCase):
    """Tests of the create club view."""

    fixtures = ['chessManagement/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('create_club')
        self.user = User.objects.get(username='johndoe@example.org')
        self.form_input = {
            'name':'KCL-Chess-Society',
            'location':'London',
            'description':'The official KCL Chess Society.'
        }

    def test_get_create_club_url(self):
        self.assertEqual(self.url,'/create_club/')

    def test_get_create_club(self):
        self.client.login(username='johndoe@example.org', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_club.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, createClubForm))
        self.assertFalse(form.is_bound)

    def test_unsuccesful_create(self):
        self.client.login(username='johndoe@example.org', password='Password123')
        self.form_input['name'] = ''
        before_count = Club.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_club.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, createClubForm))
        self.assertTrue(form.is_bound)

    def test_succesful_create(self):
        self.client.login(username='johndoe@example.org', password='Password123')
        before_count = Club.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count+1)
        club = Club.objects.get(name='KCL-Chess-Society')
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(club.name, 'KCL-Chess-Society')
        self.assertEqual(club.location, 'London')
        self.assertEqual(club.description, 'The official KCL Chess Society.')
