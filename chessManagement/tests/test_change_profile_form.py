
"""Unit tests of the log in form."""
from django import forms
from django.test import TestCase
from chessManagement.forms import changeProfile


class ChangePasswordTestCase(TestCase):
    """Unit tests of the log in form."""
    def setUp(self):
        self.form_input = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.org',
            'experience': 'Beginner',
            'bio': 'Hi I would like to apply',
            'personal_statement': 'Hello, I am John Doe.',
        }

    def test_form_contains_required_fields(self):
        form = changeProfile()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('experience', form.fields)
        self.assertIn('email', form.fields)
        self.assertIn('bio', form.fields)
        self.assertIn('personal_statement', form.fields)
        bio_field = form.fields['bio']
        personal_statement_field = form.fields['personal_statement']
        self.assertTrue(isinstance(bio_field.widget, forms.Textarea))
        self.assertTrue(isinstance(personal_statement_field.widget, forms.Textarea))

    def test_form_rejects_blank_input(self):
        self.form_input = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'experience': '',
            'bio': '',
            'personal_statement': '',
        }
        form = changeProfile(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_invalid_email(self):
        self.form_input['email'] = 'pwd'
        form = changeProfile(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_blank_bio(self):
        self.form_input['bio'] = ' '
        form = changeProfile(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_blank_personal_statement(self):
        self.form_input['personal_statement'] = ' '
        form = changeProfile(data=self.form_input)
        self.assertTrue(form.is_valid())

