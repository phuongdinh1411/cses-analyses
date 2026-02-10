# Problem from Codeforces
# http://codeforces.com/problemset/problem/892/B
#
# Problem: Wrath (Survivors)
#
# n people stand in a line (positions 1 to n, left to right). Each person i
# has a weapon that can kill L[i] people to their left. At time 0, everyone
# swings simultaneously. A person survives if they are not killed by anyone
# to their right.
#
# Count how many people survive after everyone swings.
#
# Input:
# - Line 1: Integer n (number of people)
# - Line 2: n integers L[i] (kill range for each person)
#
# Output: Number of survivors
#
# Approach: Process from right to left, tracking the leftmost position
# that will be killed by someone to the right.
# - kill_reach tracks the leftmost index that is guaranteed to be killed
# - A person at index i survives if i < kill_reach (not in kill zone)
# - Time complexity: O(n)

n = int(input())
L = list(map(int, input().split()))

survivors = 0
kill_reach = n  # Leftmost position that will be killed (initially beyond array)

for i in range(n - 1, -1, -1):
    if i < kill_reach:
        # Person i is not killed by anyone to their right
        survivors += 1
    # Person i can kill people in range [max(0, i - L[i]), i - 1]
    # Update kill_reach to be the minimum of current reach and i - L[i]
    kill_reach = min(kill_reach, i - L[i])

print(survivors)
