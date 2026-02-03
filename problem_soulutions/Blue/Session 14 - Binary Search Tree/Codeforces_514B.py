# Problem from Codeforces
# http://codeforces.com/problemset/problem/514/B
#
# Problem Name: Han Solo and Lazer Gun (Codeforces 514B)
#
# Problem Description:
# Han Solo is at position (x0, y0) and needs to shoot n stormtroopers.
# A single laser shot can kill all stormtroopers on the same ray from Han.
# Find the minimum number of shots needed to eliminate all stormtroopers.
#
# Input Format:
# - First line: n x0 y0 (number of stormtroopers, Han's position)
# - Next n lines: x y (coordinates of each stormtrooper)
#
# Output Format:
# - Minimum number of shots (distinct rays) needed
#
# Key Approach/Algorithm:
# - Two points are on the same ray if they have the same angle from origin
# - For each stormtrooper, compute angle (or slope) relative to Han's position
# - Use a set to count distinct angles/slopes
# - Stormtroopers with same slope are on the same ray


def solution():
    n, x0, y0 = map(int, input().strip().split())
    shots = set()
    for i in range(n):
        x, y = map(int, input().strip().split())
        x, y = x - x0, y - y0
        angle = 1e4
        if y != 0:
            angle = x / y
        shots.add(angle)

    print(len(shots))


solution()
