""" Schedules games in tournaments """

def assign_to_groups(players):
    groups = []
    number_of_players = len(players)
    if number_of_players > 16: # group stage
        if number_of_players > 32:
            groups = assign_to_elimination_groups(players, 6)
        else:
            groups = assign_to_elimination_groups(players, 4)
    else: # main bracket
        if number_of_players in [2,4,8,16]:
            groups = assign_to_pairs(players)
        else: # elimination stage is needed
            if number_of_players > 6:
                groups = assign_to_elimination_groups(players, 4)
            else:
                groups = assign_to_elimination_groups(players, 6)
    return groups

def assign_to_pairs(players):
    pairs = []
    i = 0
    l = len(players)
    if l % 2 == 0:
        while i < l:
            pairs.append((players[i], players[i + 1]))
            i = i + 2
    return pairs

def assign_to_elimination_groups(players, group_size):
    number_of_players = len(players)
    number_of_groups = int(number_of_players / group_size)
    groups = []
    for i in range(0, number_of_groups):
        group = []
        start = i * group_size
        end = start + group_size
        for j in range(start, end):
            group.append(players[j])
        groups.append(group)
    if number_of_players % group_size != 0:
        extra_group = []
        for i in range(group_size * number_of_groups, number_of_players):
            extra_group.append(players[i])
        if len(extra_group) < 3  and len(groups) > 1:
            extra_group.append(groups[0].pop())
            extra_group.append(groups[1].pop())
        groups.append(extra_group)
    return groups


def schedule_matches_within_group(group):
    if len(group) % 2 == 0:
        return schedule_even_draw(group)
    else:
        return schedule_odd_draw(group)

def schedule_even_draw(group):
    matches = []
    half_len = int(len(group)/2)
    arr1 = [i+1 for i in range(half_len)]
    arr2 = [i+1 for i in range(half_len, len(group))][::-1]
    for i in range(len(group)-1):
        arr1.insert(1, arr2.pop(0))
        arr2.append(arr1.pop())
        for gm in zip(arr1, arr2):
            matches.append((group[gm[0]-1], group[gm[1]-1]))
    return matches

def schedule_odd_draw(group):
    matches = []
    half_len = int((len(group)+1)/2)
    arr1 = [i+1 for i in range(half_len)]
    arr2 = [i+1 for i in range(half_len, len(group)+1)][::-1]
    for i in range(len(group)):
        arr1.insert(1, arr2.pop(0))
        arr2.append(arr1.pop())
        for gm in zip(arr1, arr2):
            if len(group)+1 not in gm:
                matches.append((group[gm[0]-1], group[gm[1]-1]))
    return matches


def reorder(list):
    new_list = []
    i = 0
    l = len(list)
    while i < int(l/2):
        new_list.append(list[i])
        i = i + 1
        new_list.append(list[l-i])
    return new_list
