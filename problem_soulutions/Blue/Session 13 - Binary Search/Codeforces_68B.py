# Problem from Codeforces
# http://codeforces.com/problemset/problem/68/B
#
# Problem Name: Energy exchange (Codeforces 68B)
#
# Problem Description:
# There are n accumulators with different energy levels. Energy can be
# transferred between accumulators, but k% is lost during transfer.
# Find the maximum equal energy level all accumulators can achieve.
#
# Input Format:
# - First line: n k (number of accumulators, loss percentage)
# - Second line: n integers (initial energy levels of accumulators)
#
# Output Format:
# - Maximum energy level achievable for all accumulators (with 9 decimal precision)
#
# Key Approach/Algorithm:
# - Binary search on the answer (target energy level)
# - For a given target, calculate energy needed by accumulators below target
# - Calculate energy available from accumulators above target (accounting for k% loss)
# - Target is achievable if available energy >= needed energy


def check_possibility(_accumulators, max_value, n, k):
    less = 0
    more = 0
    for i in range(n):
        if _accumulators[i] > max_value:
            more += _accumulators[i] - max_value
        else:
            less += max_value - _accumulators[i]

    return more - k * more / 100 >= less


def solution():
    n, k = map(int, input().strip().split())
    accumulators = list(map(int, input().strip().split()))

    lo = 0
    hi = 1000
    for i in range(100):
        mid = (lo + hi) / 2
        if check_possibility(accumulators, mid, n, k):
            lo = mid
        else:
            hi = mid

    print('{0:.9f}'.format(lo))


solution()


