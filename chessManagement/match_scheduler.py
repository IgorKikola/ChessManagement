""" Schedules games in tournaments """



def schedule(teams):
    """Return the list of games."""
    if len(teams) % 2 == 0:
        return schedule_even_draw(teams)
    else:
        return schedule_odd_draw(teams)

def schedule_even_draw(teams):
    """Return the list of games."""
    matches = []
    half_len = int(len(teams)/2)
    arr1 = [i+1 for i in range(half_len)]
    arr2 = [i+1 for i in range(half_len, len(teams))][::-1]
    for i in range(len(teams)-1):
        arr1.insert(1, arr2.pop(0))
        arr2.append(arr1.pop())
        for gm in zip(arr1, arr2):
            matches.append((teams[gm[0]-1], teams[gm[1]-1]))
    return matches

def schedule_odd_draw(teams):
    """Return the list of games."""
    matches = []
    half_len = int((len(teams)+1)/2)
    arr1 = [i+1 for i in range(half_len)]
    arr2 = [i+1 for i in range(half_len, len(teams)+1)][::-1]
    for i in range(len(teams)):
        arr1.insert(1, arr2.pop(0))
        arr2.append(arr1.pop())
        for gm in zip(arr1, arr2):
            if len(teams)+1 not in gm:
                matches.append((teams[gm[0]-1], teams[gm[1]-1]))
    return matches
