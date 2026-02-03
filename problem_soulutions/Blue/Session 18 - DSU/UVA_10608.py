# Problem from UVA
# https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=1549
#
# Problem: Friends (UVA 10608)
#
# Description:
# In a town with N citizens and M friendship relations, find the size of
# the largest group of friends. A group is defined as people connected
# directly or indirectly through friendships.
#
# Input:
# - T (test cases)
# - For each test case:
#   - N (citizens), M (friendships)
#   - M lines: u, v (u and v are friends)
#
# Output:
# - For each test case: size of the largest friend group
#
# Approach:
# - Use DSU with size tracking
# - When unioning two groups, combine their sizes
# - Track and return the maximum group size seen


parent = []
ranks = []
members = []


def make_set(N):
    global parent, ranks, members
    parent = [i for i in range(N + 5)]
    ranks = [0 for i in range(N + 5)]
    members = [1 for i in range(N + 5)]


def find_set(u):
    if parent[u] != u:
        parent[u] = find_set(parent[u])
    return parent[u]


def union_set(u, v):
    up = find_set(u)
    vp = find_set(v)

    if up == vp:
        return members[vp]
    if ranks[up] > ranks[vp]:
        parent[vp] = up
        members[up] = members[up] + members[vp]
        return members[up]
    elif ranks[up] < ranks[vp]:
        parent[up] = vp
        members[vp] = members[vp] + members[up]
        return members[vp]
    else:
        parent[up] = vp
        ranks[vp] += 1
        members[vp] = members[vp] + members[up]
        return members[vp]


def solution():

    T = int(input())
    for t in range(T):
        N, M = map(int, input().split())

        max_members = 1

        make_set(N)
        for i in range(M):
            u, v = map(int, input().split())
            current_members = union_set(u, v)
            if max_members < current_members:
                max_members = current_members

        print(max_members)


solution()

