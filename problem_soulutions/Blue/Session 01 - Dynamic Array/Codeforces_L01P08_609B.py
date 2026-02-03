# Problem from Codeforces
# http://codeforces.com/problemset/problem/609/B
#
# Problem: The Best Gift
#
# There are n books of m different genres. Tanya wants to choose 2 books of
# DIFFERENT genres as a gift. Count the number of ways to choose such a pair.
#
# Input:
# - Line 1: n m (number of books, number of genres)
# - Line 2: n integers (genre of each book, values from 1 to m)
#
# Output: Number of ways to choose 2 books of different genres
#
# Approach: Count books per genre, then sum count[i] * count[j] for all i < j


n, m = map(int, input().split())
a = list(map(int, input().split()))

total = 0
type_list = [0] * m
for i in range(n):
    type_list[a[i] - 1] += 1
for j in range(m - 1):
    for k in range(j + 1, m):
        total += type_list[j] * type_list[k]
print(total)