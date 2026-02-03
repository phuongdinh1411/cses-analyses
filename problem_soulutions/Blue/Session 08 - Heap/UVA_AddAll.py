#  Problem from UVA
#  https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1895
#
# Problem: UVA 10954 - Add All
#
# Given N numbers, you need to add them all together. Each addition operation
# costs the sum of the two numbers being added. Find the minimum total cost
# to combine all numbers into one.
#
# Input:
# - Multiple test cases until N=0
# - Line 1: N
# - Line 2: N integers
#
# Output: Minimum total cost for each test case
#
# Example: Numbers [1, 2, 3] -> Add 1+2=3 (cost 3), then 3+3=6 (cost 6) = 9
#          Better: Add 1+2=3 (cost 3), then 3+3=6 (cost 6) = 9
#          Or: 1+3=4 (cost 4), 4+2=6 (cost 6) = 10 (worse)
#
# Approach: Huffman-like algorithm - always add two smallest (use min-heap)


import heapq


def solution():
    while True:
        N = int(input())
        if N == 0:
            return
        array = list(map(int, input().strip().split()))
        heapq.heapify(array)
        sum = 0
        while len(array) > 1:
            first = heapq.heappop(array)
            second = heapq.heappop(array)
            sum += (first + second)
            heapq.heappush(array, first + second)

        print(sum)


solution()
