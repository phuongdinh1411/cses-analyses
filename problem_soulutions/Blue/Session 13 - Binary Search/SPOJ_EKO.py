# Problem from SPOJ
# https://www.spoj.com/problems/EKO/
#
# Problem Name: EKO - Eko (SPOJ)
#
# Problem Description:
# A woodcutter needs to collect at least M meters of wood. He sets a saw height H
# and cuts all trees taller than H. The wood collected from each tree is
# (tree_height - H) if tree_height > H, otherwise 0. Find the maximum H such
# that at least M meters of wood is collected.
#
# Input Format:
# - First line: N M (number of trees, required wood)
# - Second line: N integers (heights of trees)
#
# Output Format:
# - Maximum integer height H to collect at least M meters of wood
#
# Key Approach/Algorithm:
# - Binary search on the answer (saw height H)
# - For a given height, calculate total wood collected
# - If total >= M, try higher H (to maximize H)
# - If total < M, try lower H


def check_possibility(_accumulators, max_value, n, k):

    total = 0
    for i in range(n):
        if _accumulators[i] > max_value:
            total += _accumulators[i] - max_value

    return total >= k


def solution():
    n, k = map(int, input().strip().split())
    trees = list(map(int, input().strip().split()))

    lo = 0
    hi = int(2e9)
    while lo < hi - 1:
        mid = (lo + hi) // 2
        if check_possibility(trees, mid, n, k):
            lo = mid
        else:
            hi = mid

    print(lo)


solution()
