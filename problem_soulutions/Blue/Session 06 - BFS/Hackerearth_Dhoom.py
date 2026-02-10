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


from collections import deque


def find_minimum_time(key_value, lock_value, magic_numbers):
    if key_value == lock_value:
        return 0

    visited = [False] * 100000
    distance = [-1] * 100000

    q = deque()
    q.append(key_value)
    # Fixed: Mark starting state as visited
    visited[key_value] = True
    distance[key_value] = 0

    while q:
        u = q.popleft()
        for magic in magic_numbers:
            new_key = (magic * u) % 100000
            if not visited[new_key]:
                visited[new_key] = True
                distance[new_key] = distance[u] + 1
                if new_key == lock_value:
                    return distance[new_key]
                q.append(new_key)

    return -1


def solution():
    key_value, lock_value = map(int, input().split())
    N = int(input())
    magic_numbers = list(map(int, input().split()))

    print(find_minimum_time(key_value, lock_value, magic_numbers))


solution()
