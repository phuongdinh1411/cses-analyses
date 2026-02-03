# Problem from Codeforces
# http://codeforces.com/problemset/problem/673/A
#
# Problem: Bear and Game
#
# A bear watches a 90-minute football game on TV. There are n interesting
# moments at times t[1], t[2], ..., t[n] (in increasing order). The bear
# turns off the TV if more than 15 consecutive minutes pass without any
# interesting moment. Determine at what minute he stops watching.
#
# Input:
# - Line 1: Integer n (number of interesting moments)
# - Line 2: n integers t[i] (times of interesting moments, 1 <= t[i] <= 90)
#
# Output: The minute when the bear stops watching
#
# Example: n=3, times=[7,20,88] → 35 (gap from 20 to 88 > 15, stops at 20+15)


def calc_mins(_t, _n):
    if _t[0] > 15:
        return 15
    for i in range(1, _n):
        if _t[i] - _t[i - 1] > 15:
            return t[i - 1] + 15
    if 90 - _t[_n - 1] > 15:
        return _t[n - 1] + 15
    return 90


n = int(input())
t = list(map(int, input().split()))
print(calc_mins(t, n))
