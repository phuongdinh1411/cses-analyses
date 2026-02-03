# Problem from Codeforces
# http://codeforces.com/problemset/problem/242/B
#
# Problem: Big Segment
#
# Given n segments [l[i], r[i]], find if there exists a segment that completely
# covers all other segments (i.e., its left endpoint is the minimum of all left
# endpoints AND its right endpoint is the maximum of all right endpoints).
# If such a segment exists, output its 1-based index. Otherwise, output -1.
#
# Input:
# - Line 1: Integer n (number of segments)
# - Next n lines: l[i] r[i] (left and right endpoints of segment i)
#
# Output: Index of the covering segment (1-based), or -1 if none exists
#
# Example: Segments [1,5], [2,3], [1,10] → 3 (segment [1,10] covers all)


def check_cover(_l, _r, _n):
    min_left, max_right = _l[0], _r[0]
    pos = 0
    for i in range(1, n):
        if _l[i] < min_left:
            min_left = _l[i]
            if _r[i] >= max_right:
                pos = i
                max_right = _r[i]
            else:
                pos = -2
        elif _r[i] > max_right:
            max_right = _r[i]
            if _l[i] <= min_left:
                pos = i
                min_left = _l[i]
            else:
                pos = -2
        elif _l[i] == min_left and _r[i] == max_right:
            pos = i

    return pos + 1


n = int(input())
l, r = [], []
for i in range(n):
    li, ri = map(int, input().split())
    l.append(li)
    r.append(ri)
print(check_cover(l, r, n))
