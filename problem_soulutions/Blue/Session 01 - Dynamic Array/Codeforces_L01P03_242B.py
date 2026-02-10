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
#
# Approach:
# 1. Find the global minimum left endpoint and maximum right endpoint
# 2. Find any segment that has both min_left and max_right
# Time complexity: O(n)


def find_covering_segment(left_endpoints, right_endpoints, num_segments):
    # Find global min left and max right
    min_left = min(left_endpoints)
    max_right = max(right_endpoints)

    # Find a segment that matches both bounds
    for i in range(num_segments):
        if left_endpoints[i] == min_left and right_endpoints[i] == max_right:
            return i + 1  # 1-based index

    return -1


n = int(input())
l, r = [], []
for i in range(n):
    li, ri = map(int, input().split())
    l.append(li)
    r.append(ri)

print(find_covering_segment(l, r, n))
