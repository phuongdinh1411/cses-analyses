# Problem from ACM TIMUS
# http://acm.timus.ru/problem.aspx?space=1&num=1837
#
# Problem: Isenbaev's Number
#
# Description:
# In competitive programming, "Isenbaev's Number" represents the shortest
# chain of teammates connecting a person to Isenbaev (similar to Erdos number).
# Given a list of 3-person teams, calculate each person's Isenbaev number.
# Isenbaev himself has number 0, his teammates have number 1, etc.
#
# Input:
# - First line: n (number of teams)
# - Next n lines: three space-separated names (team members)
#
# Output:
# - For each unique name (in alphabetical order), print:
#   "name number" or "name undefined" if not connected to Isenbaev
#
# Approach:
# - Build an adjacency list of teammates
# - Use BFS from Isenbaev to find shortest paths to all reachable people
# - Sort and output results alphabetically

from collections import deque, defaultdict


def solution():
    n_teams = int(input())

    # Build adjacency list of teammates
    teammates = defaultdict(set)
    all_players = set()

    for _ in range(n_teams):
        team = input().split()
        all_players.update(team)
        # Each pair of team members are teammates
        for i in range(3):
            for j in range(3):
                if i != j:
                    teammates[team[i]].add(team[j])

    # BFS from Isenbaev to find shortest paths
    distance = {}
    if 'Isenbaev' in all_players:
        distance['Isenbaev'] = 0
        queue = deque(['Isenbaev'])

        while queue:
            person = queue.popleft()
            for teammate in teammates[person]:
                if teammate not in distance:
                    distance[teammate] = distance[person] + 1
                    queue.append(teammate)

    # Output results in alphabetical order
    for name in sorted(all_players):
        if name in distance:
            print(f'{name} {distance[name]}')
        else:
            print(f'{name} undefined')


solution()
