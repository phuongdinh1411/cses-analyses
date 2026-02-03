#  Problem from Hackerearth
#  https://www.hackerearth.com/ja/practice/algorithms/graphs/breadth-first-search/practice-problems/algorithm/dhoom-4/description/
#
# Problem: Dhoom 4
#
# You have a key with value K and need to unlock a lock with value L.
# You also have N magic numbers. Each time you can multiply your key value
# by any magic number, taking the result modulo 100000.
#
# Find the minimum number of operations to transform key value K into lock
# value L. If impossible, return -1.
#
# Input:
# - Line 1: K L (initial key value, target lock value)
# - Line 2: N (number of magic numbers)
# - Line 3: N integers (the magic numbers)
#
# Output: Minimum operations to reach lock value, or -1 if impossible
#
# Approach: BFS where each state is a key value (0-99999), edges are
#           multiplications by magic numbers


import queue


def find_minimum_time(key_value, lock_value, keys):

    if key_value == lock_value:
        return 0

    visited = [False for i in range(100000)]
    path = [-1 for i in range(100000)]
    q = queue.Queue()
    q.put(key_value)

    while not q.empty():
        u = q.get()
        for key in keys:
            new_key = (key * u) % 100000
            if not visited[new_key]:
                visited[new_key] = True
                q.put(new_key)
                path[new_key] = u
                if lock_value == new_key:
                    return get_time(key_value, lock_value, path)

    return -1


def get_time(key_value, lock_value, path):
    total_time = 0
    current_node = lock_value
    while True:
        if key_value == path[current_node]:
            return total_time + 1
        else:
            total_time += 1
            current_node = path[current_node]


def solution():
    key_value, lock_value = map(int, input().split())
    N = int(input())
    keys = list(map(int, input().split()))

    print(find_minimum_time(key_value, lock_value, keys))


solution()
