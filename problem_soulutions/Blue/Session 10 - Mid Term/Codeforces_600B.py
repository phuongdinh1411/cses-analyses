# Problem from Codeforces
# http://codeforces.com/problemset/problem/600/B
#
# Problem Name: Queries about less or equal elements
#
# Problem Description:
# Given two arrays A and B, for each element b[i] in B, find how many
# elements in A are less than or equal to b[i].
#
# Input Format:
# - First line: n m (sizes of arrays A and B)
# - Second line: n integers (array A)
# - Third line: m integers (array B)
#
# Output Format:
# - m integers: for each b[i], the count of elements in A that are <= b[i]
#
# Key Approach/Algorithm:
# - Sort array A
# - For each query b[i], use binary search (bisect_right) to find
#   the position where b[i] would be inserted, which gives the count

import bisect


def solution():
    n, m = map(int, input().strip().split())
    a = list(map(int, input().strip().split()))
    b = list(map(int, input().strip().split()))

    a.sort()

    for i in range(m - 1):
        print(bisect.bisect_right(a, b[i]), end=' ')
        # print(binary_search(a, b[i], -1, n), end=' ')
    print(bisect.bisect_right(a, b[m - 1]))


solution()
