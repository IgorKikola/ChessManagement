"""Unit tests for the User model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from chessManagement.models import User, Club, UserInClub

class ClubModelTestCase(TestCase):
    """Unit tests for the User model."""

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

    def test_valid_user_in_club(self):
        self._assert_user_in_club_is_valid()

    def test_user_and_club_in_userInClub_should_be_unique(self):
        try:
            second_userInClub = UserInClub.objects.create(
                user=self.user,
                club=self.club,
                user_level=3
            )
        except Exception as exception:
            ValidationError('user and club should be unique together')

    def test_user_level_can_be_0(self):
        self.userInClub.user_level = 0
        self._assert_user_in_club_is_valid()

    def test_user_level_can_be_1(self):
        self.userInClub.user_level = 1
        self._assert_user_in_club_is_valid()

    def test_user_level_can_be_2(self):
        self.userInClub.user_level = 2
        self._assert_user_in_club_is_valid()

    def test_user_level_can_be_3(self):
        self.userInClub.user_level = 3
        self._assert_user_in_club_is_valid()

    def test_user_level_can_not_be_4(self):
        self.userInClub.user_level = 4
        self._assert_user_in_club_is_invalid()

    def _assert_user_in_club_is_valid(self):
        try:
            self.userInClub.full_clean()
        except (ValidationError):
            self.fail('Test club should be valid')

    def _assert_user_in_club_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.userInClub.full_clean()
