# Problem from Codeforces
# http://codeforces.com/problemset/problem/424/B
#
# Problem: Megacity
#
# Description:
# The city of Berland wants to become a megacity (population >= 1,000,000).
# There are n locations around the city, each at coordinates (x, y) with k people.
# The city can expand its borders to a circle of radius r centered at origin (0,0).
# Find the minimum radius r such that the city population reaches 1,000,000.
#
# Input:
# - First line: n (number of locations) and s (current city population)
# - Next n lines: x, y, k (coordinates and population of each location)
#
# Output:
# - Minimum radius r (to 7 decimal places) to reach population 1,000,000
# - Print -1 if impossible
#
# Approach:
# - Calculate distance from origin to each location
# - Sort locations by distance
# - Greedily add locations (closest first) until population >= 1,000,000
# - Uses dictionary/sorting for efficient location management


import math


class Location:
    def __init__(self, r, k):
        self.r = r
        self.k = k

    def __lt__(self, other):
        return self.r < other.r


def solution():
    n, s = map(int, input().split())
    locations = []
    for i in range(n):
        x, y, k = map(int, input().split())
        locations.append(Location(math.sqrt(x*x + y*y), k))

    locations.sort()

    min_r = 0
    for i in range(n):
        if s >= 1000000:
            print(round(min_r, 7))
            return
        s += locations[i].k
        min_r = locations[i].r

    if s >= 1000000:
        print(round(min_r, 7))
    else:
        print(-1)


solution()
