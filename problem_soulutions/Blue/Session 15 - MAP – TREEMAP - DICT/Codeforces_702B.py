# Problem from Codeforces
# http://codeforces.com/problemset/problem/702/B
#
# Problem: Powers of Two
#
# Description:
# Given an array of n integers, count the number of pairs (i, j) where i < j
# such that a[i] + a[j] is a power of 2.
#
# Input:
# - First line: n (number of elements)
# - Second line: n space-separated integers a[1], a[2], ..., a[n]
#
# Output:
# - Single integer: number of pairs whose sum is a power of 2
#
# Approach:
# - Use a dictionary (hash map) to store frequency of each number seen so far
# - For each element, check all powers of 2 (up to 2^60) and count pairs
# - For each power p, if (p - a[i]) exists in dictionary, add its count
# - Time complexity: O(n * 60) using hash map for O(1) lookups


def solution():
    n = int(input())
    a = list(map(int, input().split()))

    pow2 = [2 ** i for i in range(61)]

    total = 0
    dic = {}
    for i in range(n):
        for j in range(60):
            if pow2[j] - a[i] in dic:
                total += dic[pow2[j] - a[i]]

        if a[i] in dic:
            dic[a[i]] += 1
        else:
            dic[a[i]] = 1

    print(total)


solution()
