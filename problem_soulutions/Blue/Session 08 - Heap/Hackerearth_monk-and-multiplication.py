#  Problem from Hackerearth
#  https://www.hackerearth.com/fr/practice/data-structures/trees/heapspriority-queues/practice-problems/algorithm/monk-and-multiplication/
#
# Problem: Monk and Multiplication
#
# Given an array of N integers added one by one, after each insertion output
# the product of the three largest numbers. If fewer than 3 numbers have been
# added, output -1.
#
# Input:
# - Line 1: N (number of elements)
# - Line 2: N space-separated integers
#
# Output: N lines, each containing the product of 3 largest so far, or -1
#
# Approach: Maintain a min-heap of size 3 with the largest elements


import heapq


def solution():
    N = int(input())
    A = list(map(int, input().split()))

    if N < 3:
        print(-1)
        if N > 1:
            print(-1)
        return

    max_list = A[:3]
    heapq.heapify(max_list)

    for i in range(N):
        if i < 3:
            if i == 2:
                print(max_list[0]*max_list[1]*max_list[2])
            else:
                print(-1)
        else:
            if A[i] > max_list[0]:
                heapq.heappop(max_list)
                heapq.heappush(max_list, A[i])
            print(max_list[0]*max_list[1]*max_list[2])


solution()
