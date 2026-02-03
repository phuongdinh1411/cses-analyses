# Problem from UVA
# https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3183
#
# Problem Name: The Monkey and the Oiled Bamboo (UVA 12032)
#
# Problem Description:
# A monkey climbs a bamboo ladder with rungs at given heights. The monkey starts
# with strength k and can jump up to k units. After a maximum-strength jump,
# strength decreases by 1. Find the minimum initial strength k to reach the top.
#
# Input Format:
# - T: number of test cases
# - For each test case:
#   - N: number of rungs
#   - N integers: heights of rungs from ground
#
# Output Format:
# - For each case: "Case X: k" where k is minimum initial strength needed
#
# Key Approach/Algorithm:
# - Binary search on the answer (initial strength k)
# - For each k, simulate: check if monkey can reach top
# - If current jump equals remaining strength, decrease strength
# - If any jump exceeds strength, k is insufficient
# import sys


def check_possibility(rungs, k, n):

    remain = k
    if rungs[0] > remain:
        return False
    if rungs[0] == remain:
        remain -= 1
    for i in range(1, n):
        if rungs[i] - rungs[i - 1] > remain:
            return False
        if rungs[i] - rungs[i-1] == remain:
            remain -= 1

    return remain >= 0


def solution():
    T = int(input())
    for i in range(T):
        N = int(input())
        rungs = list(map(int, input().strip().split()))

        lo = 0
        hi = int(1e7)
        while lo < hi - 1:
            mid = (lo + hi) // 2
            if check_possibility(rungs, mid, N):
                hi = mid
            else:
                lo = mid

        print('Case {0}: {1}'.format(i + 1, hi))


solution()

