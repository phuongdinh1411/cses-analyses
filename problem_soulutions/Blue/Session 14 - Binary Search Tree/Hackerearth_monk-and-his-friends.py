#  Problem from Hackerearth
#  https://www.hackerearth.com/fr/practice/data-structures/trees/binary-search-tree/practice-problems/algorithm/monk-and-his-friends/description/
#
# Problem Name: Monk and his Friends
#
# Problem Description:
# Monk is waiting for his friends in a classroom. N friends are already inside.
# M more friends arrive one by one. When a friend arrives, check if someone
# with the same ID is already in the class. After checking, the friend enters.
#
# Input Format:
# - T: number of test cases
# - For each test case:
#   - N M: friends already inside, friends arriving
#   - N+M integers: IDs (first N already inside, next M arriving)
#
# Output Format:
# - For each arriving friend: "YES" if duplicate exists, "NO" otherwise
#
# Key Approach/Algorithm:
# - Use a set to store IDs of friends inside the class
# - For each arriving friend, check if ID exists in set
# - Add the arriving friend's ID to the set after checking


def check_exist(_in, _out):
    inside_class = set(_in)
    for stu in _out:
        if stu in inside_class:
            print('YES')
        else:
            print('NO')
        inside_class.add(stu)


def solution():
    T = int(input())
    for i in range(T):
        N, M = map(int, input().strip().split())
        A = list(map(int, input().strip().split()))
        inside_class = A[:N]
        outside_class = A[N:]
        check_exist(inside_class, outside_class)


solution()
