"""Unit tests for the User model."""
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from chessManagement.models import User, Club, UserInClub

class ClubModelTestCase(TestCase):
    """Unit tests for the User model."""

    fixtures = [
        'chessManagement/tests/fixtures/default_user.json',
        'chessManagement/tests/fixtures/default_club.json',
        'chessManagement/tests/fixtures/other_clubs.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.club = Club.objects.get(name='KCL-Chess-Society')
        self.second_club = Club.objects.get(name='Another-Club')
        UserInClub.objects.create(
            user=self.user,
            club=self.club,
            user_level=3
        )
        UserInClub.objects.create(
            user=self.user,
            club=self.second_club,
            user_level=3
        )

    def test_valid_club(self):
        self._assert_club_is_valid()

    def test_name_need_be_unique(self):
        with self.assertRaises(IntegrityError):
            invalid_club = Club.objects.create(
                name=self.club.name,
                location="",
                description=""
            )

    def test_name_may_contain_50_characters(self):
        self.club.name = 'x' * 50
        self._assert_club_is_valid()

    def test_name_must_not_contain_more_than_50_characters(self):
        self.club.name = 'x' * 51
        self._assert_club_is_invalid()

    def test_location_can_not_be_blank(self):
        self.club.location = ''
        self._assert_club_is_invalid()

    def test_location_can_be_not_unique(self):
        self.club.location = self.second_club.location
        self._assert_club_is_valid()

    def test_location_may_contain_50_characters(self):
        self.club.location = 'x' * 50
        self._assert_club_is_valid()

    def test_location_must_not_contain_more_than_51_characters(self):
        self.club.location = 'x' * 51
        self._assert_club_is_invalid()

    def test_description_can_be_blank(self):
        self.club.description = ''
        self._assert_club_is_valid()

    def test_description_can_be_not_unique(self):
        self.club.description = self.second_club.description
        self._assert_club_is_valid()

    def test_description_may_contain_520_characters(self):
        self.club.description = 'x' * 520
        self._assert_club_is_valid()

    def test_description_must_not_contain_more_than_521_characters(self):
        self.club.description = 'x' * 521
        self._assert_club_is_invalid()

    def _assert_club_is_valid(self):
        try:
            self.club.full_clean()
        except (ValidationError):
            self.fail('Test club should be valid')

    def _assert_club_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.club.full_clean()
