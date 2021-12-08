"""Unit tests of the sign up form."""
from django.contrib.auth.hashers import check_password
from django import forms
from django.test import TestCase
from chessManagement.forms import createClubForm
from chessManagement.models import User, Club, UserInClub

class SignUpFormTestCase(TestCase):
    """Unit tests of the sign up form."""
    fixtures = [
        'chessManagement/tests/fixtures/default_user.json',
        'chessManagement/tests/fixtures/default_club.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.club = Club.objects.get(name='KCL-Chess-Society')
        self.userInClub = UserInClub.objects.create(
            user=self.user,
            club=self.club,
            user_level=3
        )
        self.form_input = {
            'name': 'ClubName',
            'location': 'ClubLocation',
            'description': 'ClubDescription'
        }

    def test_valid_sign_up_form(self):
        form = createClubForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = createClubForm()
        self.assertIn('name', form.fields)
        self.assertIn('location', form.fields)
        self.assertIn('description', form.fields)

    def test_name_must_not_be_blanks(self):
        self.form_input['name'] = ''
        form = createClubForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_name_must_not_be_equal_to_other_club_name(self):
        self.form_input['name'] = 'KCL-Chess-Society'
        form = createClubForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_location_must_not_be_blank(self):
        self.form_input['location'] = ''
        form = createClubForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = createClubForm(data=self.form_input)
        before_count = Club.objects.count()
        form.save(self.user)
        after_count = Club.objects.count()
        self.assertEqual(after_count, before_count+1)
        club = Club.objects.get(name='ClubName')
        self.assertEqual(club.name, 'ClubName')
        self.assertEqual(club.location, 'ClubLocation')
        self.assertEqual(club.description, 'ClubDescription')
