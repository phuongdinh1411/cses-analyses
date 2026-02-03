#  Problem from SPOJ
#  https://www.spoj.com/problems/PRO/
#
# Problem: PRO - Promotion
#
# A supermarket runs a promotion over N days. Each day, some customers submit
# receipts. At the end of each day, the customer with the highest receipt wins
# prize equal to receipt value, and the lowest receipt customer wins prize
# equal to their receipt value (both are removed from future consideration).
#
# Calculate total prize money: sum(max) - sum(min) over all days.
#
# Input:
# - Line 1: N (number of days)
# - Next N lines: k r1 r2 ... rk (k receipts for that day)
#
# Output: Total prize difference
#
# Approach: Use two heaps (min and max) with lazy deletion to track receipts


import heapq


MAX = 1000005


def solution():

    n = int(input())
    sum_prizes = 0
    max_heap = []
    min_heap = []

    deleted_max = [0 for i in range(MAX)]
    deleted_min = [0 for i in range(MAX)]

    for i in range(n):
        line = list(map(int, input().strip().split()))
        num_rc = line[0]
        receipts = line[1:]
        for j in range(num_rc):
            heapq.heappush(min_heap, receipts[j])
            heapq.heappush(max_heap, -receipts[j])

        if len(max_heap) >= 2:
            from_max = heapq.heappop(max_heap)
            from_min = heapq.heappop(min_heap)
            while deleted_min[-from_max] > 0:
                deleted_min[-from_max] -= 1
                from_max = heapq.heappop(max_heap)
            while deleted_max[-from_min] > 0:
                deleted_max[-from_min] -= 1
                from_min = heapq.heappop(min_heap)

            deleted_max[from_max] += 1
            deleted_min[from_min] += 1

            sum_prizes -= (from_max + from_min)

    print(sum_prizes)


solution()
