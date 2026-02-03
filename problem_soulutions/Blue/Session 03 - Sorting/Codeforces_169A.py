# Problem from Codeforces
# http://codeforces.com/problemset/problem/169/A
#
# Problem: Chores
#
# Petya and Vasya divide n chores. They have agreed:
# - Vasya does the a "easiest" chores (lowest difficulty)
# - Petya does the b "hardest" chores (highest difficulty)
# where a + b = n.
#
# The "gap" is the difference between the easiest chore Petya does and the
# hardest chore Vasya does. After sorting, this is h[b] - h[b-1].
#
# Input:
# - Line 1: n a b (total chores, Vasya's count, Petya's count)
# - Line 2: n integers (difficulty of each chore)
#
# Output: The gap between Petya's easiest and Vasya's hardest chore
#
# Approach: Sort and find difference between position b and b-1

n, a, b = map(int, input().split())
h = list(map(int, input().split()))

h.sort()

print(h[b] - h[b - 1])
