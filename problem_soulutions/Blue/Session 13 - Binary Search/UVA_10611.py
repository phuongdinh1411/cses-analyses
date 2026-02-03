# Problem from UVA
# https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=316&page=show_problem&problem=1552
#
# Problem Name: The Playboy Chimp (UVA 10611)
#
# Problem Description:
# A male chimp wants to find a partner among N female chimps lined up by height.
# For Q male chimps with given heights, find the tallest female shorter than him
# and the shortest female taller than him.
#
# Input Format:
# - N: number of female chimps
# - N heights of female chimps (sorted in non-decreasing order)
# - Q: number of queries
# - Q heights of male chimps
#
# Output Format:
# - For each query: two values separated by space
#   - Tallest female shorter than query height (or 'X' if none)
#   - Shortest female taller than query height (or 'X' if none)
#
# Key Approach/Algorithm:
# - Use binary search (bisect_right) to find insertion point
# - For shorter: search backwards from insertion point for strictly smaller
# - For taller: the element at insertion point if it exists and is strictly greater
# import sys

from bisect import bisect_right


def solution():
    N = int(input())
    lady_chimps = list(map(int, input().strip().split()))
    Q = int(input())
    queries = list(map(int, input().strip().split()))

    for q in queries:
        upper_bound = bisect_right(lady_chimps, q)
        shorter_index = -1
        if upper_bound > 0:
            for i in range(upper_bound - 1, -1, -1):
                if lady_chimps[i] < q:
                    shorter_index = i
                    break
        shorter = 'X'
        taller = 'X'
        if shorter_index != -1:
            shorter = str(lady_chimps[shorter_index])
        if upper_bound < N:
            taller = str(lady_chimps[upper_bound])

        print(shorter, taller)


solution()


