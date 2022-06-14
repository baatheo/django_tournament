import random


def determineFirstStage(amount):
    stage = 2
    while amount > stage:
        stage *= 2
    return int(stage / 2)


def prepareMatches(stage, querySet):
    matches = []
    teams = []
    for team in querySet:
        teams.append(team)
    counter = len(teams)
    while counter < stage * 2:
        lucky = random.choice(teams)
        teams.remove(lucky)
        counter += 1
    while len(teams) > 0:
        match = {}
        first = random.choice(teams)
        teams.remove(first)
        second = random.choice(teams)
        teams.remove(second)
        match['stage'] = stage
        match['firstTeam'] = first.id
        match['secondTeam'] = second.id
        matches.append(match)
    return matches
