# Problem from Codeforces
# http://codeforces.com/problemset/problem/279/B
#
# Problem: Books
#
# Valera has n books on a shelf. Each book i takes a[i] minutes to read.
# He has t minutes of free time and wants to read as many CONSECUTIVE books
# as possible (starting from any position). Find the maximum number of
# consecutive books he can completely read within time t.
#
# Input:
# - Line 1: n t (number of books, available time)
# - Line 2: n integers (reading time for each book)
#
# Output: Maximum number of consecutive books that can be read
#
# Approach: Sliding window / two-pointer technique

n, t = map(int, input().split())
a = list(map(int, input().split()))

total_time = 0

left = 0
right = 0

max_total_book = 0
max_left = 0

while True:

    while right < n and total_time + a[right] <= t:
        total_time += a[right]
        right += 1

    while total_time > t:
        total_time -= a[left]
        left += 1

    if right - left > max_total_book:
        max_total_book = right - left
        max_left = left

    if right < n:
        total_time += a[right]
        right += 1
    else:
        break

print(max_total_book)
