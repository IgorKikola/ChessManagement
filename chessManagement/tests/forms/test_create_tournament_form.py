"""Unit tests of the create tournament form."""
from django import forms
from django.test import TestCase
from chessManagement.forms import createTournamentForm

class CreateTournamentFormTestCase(TestCase):
    """Unit tests of the create tournament form."""
    def setUp(self):
        self.form_input = {'name': 'My Tournament', 'description': 'my Tournament','deadline': '2022-11-23','max_players':56}

    def test_form_contains_required_fields(self):
        form = createTournamentForm()
        self.assertIn('name', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('deadline', form.fields)
        self.assertIn('max_players', form.fields)

    def test_form_accepts_valid_input(self):
        form = createTournamentForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_name(self):
        self.form_input['name'] = ''
        form = createTournamentForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_deadline(self):
        self.form_input['deadline'] = ''
        form = createTournamentForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_blank_description(self):
        self.form_input['description'] = ''
        form = createTournamentForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_reject_blank_max_players(self):
        self.form_input['max_players'] = ''
        form = createTournamentForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_reject_greater_than_96_max_players(self):
        self.form_input['max_players'] = 97
        form = createTournamentForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_reject_less_than_2_max_players(self):
        self.form_input['max_players'] = 1
        form = createTournamentForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_reject_less_than_today_deadline(self):
        self.form_input['deadline'] = '2012-12-11'
        form = createTournamentForm(data=self.form_input)
        self.assertFalse(form.is_valid())
