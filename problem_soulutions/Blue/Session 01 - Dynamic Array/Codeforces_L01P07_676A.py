# Problem from Codeforces
# http://codeforces.com/problemset/problem/676/A
#
# Problem: Nicholas and Permutation
#
# Given a permutation of integers 1 to n, you can perform at most one swap
# of any two elements. Find the maximum possible distance between the
# positions of elements 1 and n after the swap.
#
# Distance is defined as |pos(1) - pos(n)|.
#
# Input:
# - Line 1: Integer n
# - Line 2: A permutation of integers 1 to n
#
# Output: Maximum achievable distance between positions of 1 and n
#
# Key insight: You can move either 1 or n to an endpoint (position 0 or n-1)
#              to maximize distance. Check all 4 possibilities.


def calc_max_dist(_a, _n):
    pos_min, pos_max = 0, 0
    for i in range(_n):
        if _a[i] == n:
            pos_max = i
        if _a[i] == 1:
            pos_min = i
    return max(n - 1 - pos_max, n - 1 - pos_min, pos_max, pos_min)


n = int(input())
a = list(map(int, input().split()))
print(calc_max_dist(a, n))
