# Problem from Codeforces
# http://codeforces.com/problemset/problem/149/A
#
# Problem: Business Trip
#
# A flower must grow at least k centimeters. There are 12 months, and each
# month i has a potential growth a[i] centimeters if watered that month.
# Find the minimum number of months you need to water the flower to achieve
# at least k centimeters of growth. You can choose which months to water.
#
# Input:
# - Line 1: Integer k (required growth in centimeters)
# - Line 2: 12 integers (growth potential for each month)
#
# Output: Minimum number of months needed, or -1 if impossible
#
# Approach: Sort months by growth (descending), greedily pick highest growth months

k = int(input())
a = list(map(int, input().split()))

growth_cent = 0

a.sort(key=lambda x: -x)
for i in range(12):
    if growth_cent >= k:
        print(i)
        exit()
    growth_cent += a[i]
    if growth_cent >= k:
        print(i + 1)
        exit()

print('-1')
