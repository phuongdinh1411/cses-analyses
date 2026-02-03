# Problem from Codeforces
# http://codeforces.com/problemset/problem/572/A
#
# Problem: Arrays
#
# Given two sorted arrays a (size na) and b (size nb) in non-decreasing order,
# check if ALL of the first k elements of array a are strictly less than ALL
# of the last m elements of array b.
#
# Input:
# - Line 1: na nb (sizes of arrays)
# - Line 2: k m (number of elements to consider from each array)
# - Line 3: Array a (na integers, sorted non-decreasing)
# - Line 4: Array b (nb integers, sorted non-decreasing)
#
# Output: "YES" if condition is satisfied, "NO" otherwise
#
# Key insight: Just compare a[k-1] < b[nb-m] (max of first k vs min of last m)


def check_arrays(_a, _b, _k, _m):
    if _a[k - 1] >= _b[-m]:
        return 'NO'
    else:
        return 'YES'


na, nb = map(int, input().split())
k, m = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))
print(check_arrays(a, b, k, m))
