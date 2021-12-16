"""Unit tests for the User model."""
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from chessManagement.models import User, Club, UserInClub, Tournament, UserInTournament


class TournamentModelTestCase(TestCase):
    """Unit tests for the User model."""

    fixtures = [
        'chessManagement/tests/fixtures/default_user.json',
        'chessManagement/tests/fixtures/default_club.json',
        'chessManagement/tests/fixtures/other_clubs.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.club = Club.objects.get(name='KCL-Chess-Society')
        UserInClub.objects.create(
            user=self.user,
            club=self.club,
            user_level=3
        )
        self.tournament = Tournament.objects.create(
            name="John Tournament",
            club=self.club,
            description="this is johns tournament",
            organiser=self.user,
            max_players=56,
            deadline='2022-12-27',
            finished=False
        )
        UserInTournament.objects.create(
            user=self.user,
            tournament=self.tournament,
            is_organiser=True,
            is_co_organiser=False
        )

    def test_tournament_name(self):
        self.tournament.name = ''
        self._assert_tournament_is_invalid()

    def test_name_may_contain_120_characters(self):
        self.tournament.name = 'x' * 120
        self._assert_tournament_is_valid()

    def test_name_must_not_contain_more_than_120_characters(self):
        self.tournament.name = 'x' * 121
        self._assert_tournament_is_invalid()

    def test_description_may_be_blank(self):
        self.tournament.description= ''
        self._assert_tournament_is_valid()

    def test_description_may_contain_520_characters(self):
        self.tournament.description = 'x' * 520
        self._assert_tournament_is_valid()

    def test_description_must_not_contain_more_than_520_characters(self):
        self.tournament.description = 'x' * 521
        self._assert_tournament_is_invalid()

    def test_max_players_within_limits(self):
        self.tournament.max_players=65
        self._assert_tournament_is_valid()

    def test_max_players_outside_limits_above_98(self):
        self.tournament.max_players=98
        self._assert_tournament_is_invalid()

    def test_max_players_outside_limits_under_2(self):
        self.tournament.max_players=1
        self._assert_tournament_is_invalid()

    def test_incorrect_format_deadline(self):
        self.tournament.deadline='2011/12/11'
        self._assert_tournament_is_invalid()

    def test_correct_format_deadline(self):
        self.tournament.deadline='2022-11-11'
        self._assert_tournament_is_valid()

    def _assert_tournament_is_valid(self):
        try:
            self.tournament.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_tournament_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.tournament.full_clean()