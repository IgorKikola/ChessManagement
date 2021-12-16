from django.test import TestCase
from chessManagement.match_scheduler import assign_to_groups, schedule_matches_within_group

class matchSchedulerTest(TestCase):

    def setUp(self):
        """ Players """
        self.two_players = [1,2]
        self.five_players = [1,2,3,4,5]
        self.seven_players = [1,2,3,4,5,6,7]
        self.ten_players = [1,2,3,4,5,6,7,8,9,10]
        self.sixteen_players = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
        self.twenty_players = []
        for i in range(1,21):
            self.twenty_players.append(i)
        self.fourty_players = []
        for i in range(1,41):
            self.fourty_players.append(i)

        """ Groups """
        self.pair = (1,2)
        self.three_person_group = [1,2,3]
        self.four_person_group = [1,2,3,4]
        self.five_person_group = [1,2,3,4,5]
        self.six_person_group = [1,2,3,4,5,6]


    """ Tests for assigning into groups """

    def test_two_players_are_assigned_into_pairs(self):
        players = self.two_players
        groups = assign_to_groups(players)
        self.assertEqual(groups, [(1,2)])

    def test_five_players_are_assigned_into_one_elimination_group(self):
        players = self.five_players
        groups = assign_to_groups(players)
        self.assertEqual(groups, [[1,2,3,4,5]])

    def test_seven_players_are_assigned_into_two_elimination_groups(self):
        players = self.seven_players
        groups = assign_to_groups(players)
        self.assertEqual(groups, [[1,2,3,4],[5,6,7]])

    def test_ten_players_are_assigned_into_three_elimination_groups(self):
        players = self.ten_players
        groups = assign_to_groups(players)
        self.assertEqual(groups, [[1,2,3],[5,6,7],[9,10,4,8]])

    def test_sixteen_players_are_assigned_into_eight_pairs(self):
        players = self.sixteen_players
        groups = assign_to_groups(players)
        self.assertEqual(groups, [(1,2),(3,4),(5,6),(7,8),(9,10),(11,12),(13,14),(15,16)])

    def test_twenty_players_are_assigned_into_five_four_person_groups(self):
        players = self.twenty_players
        groups = assign_to_groups(players)
        self.assertTrue(len(groups),5)
        self.assertEqual(self._get_lowest_group_size(groups), 4)
        self.assertEqual(self._get_highest_group_size(groups), 4)

    def test_fourty_players_are_assigned_into_seven_groups(self):
        players = self.fourty_players
        groups = assign_to_groups(players)
        self.assertTrue(len(groups),7)
        self.assertEqual(self._get_lowest_group_size(groups), 4)
        self.assertEqual(self._get_highest_group_size(groups), 6)
        groups.pop()
        self.assertEqual(self._get_lowest_group_size(groups), 6)
        self.assertEqual(self._get_highest_group_size(groups), 6)


    """ Tests for scheduling matches """


    def pair_is_assigned_into_a_single_match(self):
        group = self.pair
        matches = schedule_matches_within_group(group)
        self.assertEqual(matches, [(1,2)])

    def test_three_person_group_is_assigned_matches_properly(self):
        group = self.three_person_group
        matches = schedule_matches_within_group(group)
        matches.sort()
        self.assertEqual(matches, [(1,2),(1,3),(2,3)])

    def test_four_person_group_is_assigned_matches_properly(self):
        group = self.four_person_group
        matches = schedule_matches_within_group(group)
        self.assertEqual(len(matches), 6)

    def test_five_person_group_is_assigned_matches_properly(self):
        group = self.five_person_group
        matches = schedule_matches_within_group(group)
        self.assertEqual(len(matches), 10)

    def test_six_person_group_is_assigned_matches_properly(self):
        group = self.six_person_group
        matches = schedule_matches_within_group(group)
        self.assertEqual(len(matches), 15)


    def _get_lowest_group_size(self, groups):
        lowest = 100
        for group in groups:
            if len(group) < lowest:
                lowest = len(group)
        return lowest

    def _get_highest_group_size(self, groups):
        highest = 0
        for group in groups:
            if len(group) > highest:
                highest = len(group)
        return highest
