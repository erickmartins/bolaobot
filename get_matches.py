
def get_matches(tiers, penalties):
    import pandas as pd
    from download_matches import get_today
    from download_matches import detect_next_saturday
    from download_matches import download_matches
    tiers = read_tiers_file(tiers)

    if tiers == "":
        return []

    today = get_today()
    nextsat, nextsun = detect_next_saturday(today)

    sat_matches = download_matches(nextsat)
    # sat_matches.to_csv("satmatches.txt")
    sun_matches = download_matches(nextsun)
    # sun_matches.to_csv("sunmatches.txt")
    all_matches = pd.concat([sat_matches, sun_matches])
    all_matches.to_csv("matches.txt")
    # print(all_matches)
    matches = select_matches(tiers, all_matches, penalties)
    print(matches)
    return matches

def safe_drop(frame, index):
    # print(index[0])
    # print(frame.index)
    if frame.index.contains(index[0]):
        newframe = frame.drop(index)
    else:
        newframe = frame
    return newframe



def select_matches(tiers, all_matches, penalties):
    # print(all_matches)
    import pandas as pd
    if penalties:
        # 1, 2, 3: tiers
        # 4: all tiers
        # 5: tier 1, 2 or 3
        breakdown = [1, 1, 1, 1, 2, 2, 3, 4, 5, 1, 1, 1, 2, 3]
    else:
        breakdown = [1, 1, 1, 1, 2, 2, 3, 4, 5]
    all_matches = all_matches.reset_index()
    tieredmatches = break_matches(tiers, all_matches)
    # print(tieredmatches)
    matches = []
    for match in breakdown:
        # print(match, matches)
        if tieredmatches[match - 1].empty:
            sample = tieredmatches[3].sample()
            matches.append(sample.values)
            tieredmatches[3] = tieredmatches[3].drop(sample.index)
            tieredmatches[0] = safe_drop(tieredmatches[0],sample.index)
            tieredmatches[1] = safe_drop(tieredmatches[1],sample.index)
            tieredmatches[2] = safe_drop(tieredmatches[2],sample.index)
            tieredmatches[4] = safe_drop(tieredmatches[4],sample.index)

        else:
            sample = tieredmatches[match - 1].sample()
            matches.append(sample.values)
            tieredmatches[match - 1] = tieredmatches[match -
                                                     1].drop(sample.index)
            tieredmatches[3] = safe_drop(tieredmatches[3],sample.index)
            tieredmatches[4] = safe_drop(tieredmatches[4],sample.index)


    format_matches = []
    for match in matches:
        b = list(','.join('%s' %x for x in y) for y in match)
        print(b)
        format_matches.append(b)
    return format_matches


def break_matches(tiers, matches):
    # print(matches)
    import pandas as pd
    tiered = []
    alltiers = [item for sublist in tiers for item in sublist]
    tier5 = matches[matches['league'].isin(alltiers)]
    for thistier in tiers:
        # print(type(thistier))
        # print(type(['BRAZIL SERIE A', ' BRAZIL CARIOCA', ' BRAZIL PAULISTA']))
        # print(matches['league'].isin(thistier))
        thesematches = matches[matches['league'].isin(thistier)]
        tiered.append(thesematches)
        # pd.concat([tier5, thesematches])
        # print(tier5)
    tiered.append(matches)
    tiered.append(tier5)
    # print(tiered)

    return tiered


def read_tiers_file(filename):
    try:
        f = open(filename, "r")
        tiers = []
        for line in f.readlines():
            line = line.strip()
            # elements =line.split(",")
            # for element in elements:
            tiers.append(line.rsplit(","))
        return tiers
    except IOError:
        return 0


def test_open_file():
    filename = ""
    assert get_matches(filename, True) == []


def test_read_tiers_nofile():
    filename = ""
    assert read_tiers_file(filename) == 0


def test_number_tiers():
    tiers = "tiers.txt"

    assert len(read_tiers_file(tiers)) == 3


def test_first_tier():
    tiers = "tiers.txt"
    assert read_tiers_file(tiers)[0][0] == "BRAZIL SERIE A"


def test_number_matches():
    tiers = "tiers.txt"
    assert len(get_matches(tiers, False)) == 9
    assert len(get_matches(tiers, True)) == 14


if __name__ == "__main__":
    tiers = "tiers.txt"
    get_matches(tiers, True)
