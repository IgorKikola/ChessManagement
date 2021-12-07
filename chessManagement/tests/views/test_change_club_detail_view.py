from django.test import TestCase
from django.urls import reverse
from chessManagement.models import User, Club, UserInClub
from chessManagement.tests.helpers import reverse_with_next
from chessManagement.forms import changeClubDetails

class ChangeClubDetailsTest(TestCase):

    fixtures = [
        'chessManagement/tests/fixtures/default_user.json',
        'chessManagement/tests/fixtures/default_club.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.club = Club.objects.get(name='KCL-Chess-Society')

        """This should probably be in a fixture, but it works for now."""
        UserInClub.objects.create(
            user=self.user,
            club=self.club,
            user_level=3
        )
        self.form_input = {'location': 'London', 'description': 'The official KCL Chess Society.'}
        self.client.login(username='johndoe@example.org', password='Password123')
        self.url = reverse('change_club_details', kwargs={'club_pk': self.club.pk})

    def test_show_user_url(self):
        self.assertEqual(self.url,f'/club/{self.club.pk}/change_details/')

    def test_get_change_club_detail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_club_details.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, changeClubDetails))
        self.assertFalse(form.is_bound)

    def test_successful_change_only_location(self):
        self.form_input['location'] = 'Location'
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('show_club', kwargs={'club_pk': self.club.pk})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'show_club/for_owner.html')
        chessClub = Club.objects.get(pk=self.club.pk)
        self.assertTrue(chessClub.location == "Location")
        self.assertTrue(chessClub.description == "The official KCL Chess Society.")

    def test_successful_change_only_description(self):
        self.form_input['description'] = 'Description'
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('show_club', kwargs={'club_pk': self.club.pk})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'show_club/for_owner.html')
        chessClub = Club.objects.get(pk=self.club.pk)
        self.assertTrue(chessClub.location == "London")
        self.assertTrue(chessClub.description == "Description")

    def test_successful_change_all_information(self):
        self.form_input['location'] = 'Location'
        self.form_input['description'] = 'Description'
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('show_club', kwargs={'club_pk': self.club.pk})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'show_club/for_owner.html')
        chessClub = Club.objects.get(pk=self.club.pk)
        self.assertTrue(chessClub.location == "Location")
        self.assertTrue(chessClub.description == "Description")
