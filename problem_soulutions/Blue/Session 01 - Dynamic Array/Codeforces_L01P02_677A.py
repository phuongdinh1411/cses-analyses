# Problem from Codeforces
# http://codeforces.com/problemset/problem/677/A
#
# Problem: Vanya and Fence
#
# Vanya and his n friends want to pass under a fence of height h. Each friend
# has a height a[i]. If a friend's height <= h, they walk normally (width 1).
# If taller, they must bend sideways (width 2). Calculate the total road width
# needed for all friends to pass.
#
# Input:
# - Line 1: n h (number of friends, fence height)
# - Line 2: n integers (heights of friends)
#
# Output: Total road width needed
#
# Example: n=3, h=7, heights=[4,5,14] → 4 (1+1+2)


def cal_road_width(_a, _h):
    road_width = 0
    for ai in _a:
        road_width += 1 if ai <= _h else 2
    return road_width


n, h = map(int, input().split())
a = list(map(int, input().split()))
print(cal_road_width(a, h))

