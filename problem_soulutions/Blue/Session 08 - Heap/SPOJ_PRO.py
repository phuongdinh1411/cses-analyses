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


def solution():
    n = int(input())
    sum_prizes = 0
    max_heap = []  # Store negated values for max-heap behavior
    min_heap = []

    # Lazy deletion tracking using dictionaries for efficiency
    deleted_from_max = {}  # Track values deleted via min_heap operations
    deleted_from_min = {}  # Track values deleted via max_heap operations

    for _ in range(n):
        line = list(map(int, input().strip().split()))
        num_receipts = line[0]
        receipts = line[1:]

        for receipt in receipts:
            heapq.heappush(min_heap, receipt)
            heapq.heappush(max_heap, -receipt)

        if len(max_heap) >= 2:
            # Get maximum value (remove lazy-deleted entries first)
            while max_heap and -max_heap[0] in deleted_from_max and deleted_from_max[-max_heap[0]] > 0:
                val = -heapq.heappop(max_heap)
                deleted_from_max[val] -= 1

            # Get minimum value (remove lazy-deleted entries first)
            while min_heap and min_heap[0] in deleted_from_min and deleted_from_min[min_heap[0]] > 0:
                val = heapq.heappop(min_heap)
                deleted_from_min[val] -= 1

            max_val = -heapq.heappop(max_heap)
            min_val = heapq.heappop(min_heap)

            # Mark these values as deleted in the other heap
            deleted_from_min[max_val] = deleted_from_min.get(max_val, 0) + 1
            deleted_from_max[min_val] = deleted_from_max.get(min_val, 0) + 1

            sum_prizes += max_val - min_val

    print(sum_prizes)


solution()
