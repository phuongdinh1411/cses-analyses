# Problem from Codeforces
# http://codeforces.com/problemset/problem/387/B
#
# Problem: George and Round
#
# George wants to prepare a programming contest with n problems of specific
# difficulties a[1], a[2], ..., a[n]. He has m prepared problems with
# difficulties b[1], b[2], ..., b[m]. Both arrays are sorted in non-decreasing
# order.
#
# A prepared problem with difficulty b[j] can be used for a required problem
# with difficulty a[i] if b[j] >= a[i]. Each prepared problem can be used at
# most once. Find the minimum number of NEW problems George must create.
#
# Input:
# - Line 1: n m (required problems, prepared problems)
# - Line 2: n integers (required difficulties, sorted)
# - Line 3: m integers (prepared difficulties, sorted)
#
# Output: Minimum number of new problems to create
#
# Approach: Two-pointer greedy matching

n, m = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

needed_problem_index = 0
prepared_problem_index = 0

while True:

    while prepared_problem_index < m and b[prepared_problem_index] < a[needed_problem_index]:
        prepared_problem_index += 1

    if prepared_problem_index >= m:
        break

    prepared_problem_index += 1

    needed_problem_index += 1

    if prepared_problem_index >= m:
        break

    if needed_problem_index >= n:
        break

print(n - needed_problem_index)
