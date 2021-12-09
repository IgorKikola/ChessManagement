"""Unit tests of the log in form."""
from django import forms
from django.test import TestCase
from chessManagement.forms import changeClubDetails


class ChangePasswordTestCase(TestCase):
    """Unit tests of the log in form."""
    def setUp(self):
        self.form_input = {
            'location': 'ClubLocation',
            'description': 'ClubDescription'
        }

    def test_form_contains_required_fields(self):
        form = changeClubDetails()
        self.assertIn('location', form.fields)
        self.assertIn('description', form.fields)

    def test_form_rejects_blank_location(self):
        self.form_input['location'] = ''
        form = changeClubDetails(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_blank_description(self):
        self.form_input['description'] = ''
        form = changeClubDetails(data=self.form_input)
        self.assertTrue(form.is_valid())
