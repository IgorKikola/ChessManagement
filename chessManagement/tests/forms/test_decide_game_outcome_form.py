"""Unit tests of the decide game outcome form."""
from django import forms
from django.test import TestCase
from chessManagement.forms import decideGameOutcome


class DecideGameOutcomeTest(TestCase):
    def setUp(self):
        self.form_input = {'winner': "1"}

    def test_form_contains_required_fields(self):
        form = decideGameOutcome()
        self.assertIn('winner', form.fields)
        winner_field = form.fields['winner']
        self.assertTrue(isinstance(winner_field,forms.ChoiceField))

    def test_form_accepts_valid_input(self):
        form = decideGameOutcome(data=self.form_input)
        self.assertTrue(form.is_valid())
