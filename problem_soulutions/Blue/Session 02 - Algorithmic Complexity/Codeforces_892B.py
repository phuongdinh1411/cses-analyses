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
# Approach: Process from right to left, tracking kill coverage

n = int(input())
L = list(map(int, input().split()))

total_people = n
last_kill = 0
for i in range(n - 1, 0, -1):
    if L[i] > last_kill:
        if L[i] < i:
            total_people -= (L[i] - last_kill)
            last_kill = L[i] - 1
        else:
            total_people -= (i - last_kill)
            break
    else:
        last_kill = last_kill - 1 if last_kill > 0 else 0
print(total_people)
