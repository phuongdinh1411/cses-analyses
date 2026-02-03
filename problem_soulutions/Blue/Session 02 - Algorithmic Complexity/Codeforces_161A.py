# Problem from Codeforces
# http://codeforces.com/problemset/problem/161/A
#
# Problem: Soldier and Vests
#
# There are n soldiers and m vests. Each soldier has a size a[i], and each vest
# has a size b[i]. A soldier can wear a vest if the vest size is in the range
# [a[i] - x, a[i] + y]. Both arrays are sorted in ascending order.
#
# Find the maximum number of soldiers that can receive vests, and output the
# pairs (soldier index, vest index) for each assignment.
#
# Input:
# - Line 1: n m x y (soldiers, vests, lower tolerance, upper tolerance)
# - Line 2: n integers (soldier sizes, sorted ascending)
# - Line 3: m integers (vest sizes, sorted ascending)
#
# Output:
# - Line 1: Number of soldiers who get vests
# - Next lines: Pairs of (soldier index, vest index) - 1-based
#
# Approach: Two-pointer technique on sorted arrays

n, m, x, y = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

u, v = [], []

sindex = 0
vindex = 0

while True:

    while vindex < m and a[sindex] - x > b[vindex]:  # too small
        vindex += 1  # Add vest's size

    if vindex >= m:
        break

    while sindex < n and a[sindex] + y < b[vindex]:  # too big
        sindex += 1  # Add solider's size

    if sindex >= n:
        break

    if a[sindex] - x > b[vindex]:
        continue

    u.append(sindex + 1)
    v.append(vindex + 1)

    sindex += 1
    vindex += 1

    if sindex >= n or vindex >= m:
        break

print(len(u))
for i in range(len(u)):
    print(u[i], v[i], sep=' ')
