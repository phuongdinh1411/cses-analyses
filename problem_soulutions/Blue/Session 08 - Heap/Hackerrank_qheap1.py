#  Problem from Hackerrank
#  https://www.hackerrank.com/challenges/qheap1/problem
#
# Problem: QHEAP1
#
# Implement a min-heap that supports the following operations:
# - "1 v": Add element v to the heap
# - "2 v": Delete element v from the heap (v is guaranteed to exist)
# - "3": Print the minimum element
#
# Input:
# - Line 1: Q (number of queries)
# - Next Q lines: Queries as described above
#
# Output: For each type-3 query, print the minimum element
#
# Approach: Use a heap with lazy deletion (track deleted elements separately)


#  Using not in and index is faster than checking manually using for loop
import heapq


def solution():
    Q = int(input())
    my_list = []
    delete_list = []
    for i in range(Q):
        query = input()
        if query.startswith('3'):
            while True:
                if my_list[0] not in delete_list:
                    break
                pos = delete_list.index(my_list[0])
                delete_list.pop(pos)
                heapq.heappop(my_list)

            print(my_list[0])
        else:
            command, param = map(int, query.split())
            if command == 1:
                heapq.heappush(my_list, param)
            else:
                delete_list.append(param)


solution()


#
# from queue import PriorityQueue
#
# def main():
#     n = int(input())
#     q = PriorityQueue()
#     remove = []
#     for i in range(n):
#         line = list(map(int, input().split()))
#         if line[0] == 1:
#             q.put(line[1])
#         elif line[0] == 2:
#             remove.append(line[1])
#         else:
#             while q.queue[0] in remove:
#                 remove.pop(remove.index(q.get()))
#             print(q.queue[0])
#
# if __name__ == '__main__':
#     main()