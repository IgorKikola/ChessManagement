"""Unit tests of the log in form."""
from django import forms
from django.test import TestCase
from chessManagement.forms import changePassword


class ChangeProfileTestCase(TestCase):
    """Unit tests of the log in form."""
    def setUp(self):
        self.form_input = {'new_password': "Password123", 'new_password_confirmation': 'Password123'}

    def test_form_contains_required_fields(self):
        form = changePassword()
        self.assertIn('new_password', form.fields)
        password_field = form.fields['new_password']
        self.assertTrue(isinstance(password_field.widget,forms.PasswordInput))

    def test_form_accepts_valid_input(self):
        form = changePassword(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_password(self):
        self.form_input['new_password'] = ''
        form = changePassword(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_invalid_password(self):
        self.form_input['new_password'] = 'pwd'
        form = changePassword(data=self.form_input)
        self.assertFalse(form.is_valid())
