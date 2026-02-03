# Problem from UVA
# https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=2498
#
# Problem: Virtual Friends (UVA 11503)
#
# Description:
# A social network tracks friendships. When two people become friends,
# their friend networks merge. After each friendship, output the total
# size of the merged network.
#
# Input:
# - T (test cases)
# - For each test case:
#   - F (number of friendships)
#   - F lines: name1 name2 (these two become friends)
#
# Output:
# - After each friendship: size of the resulting friend network
#
# Approach:
# - Use DSU with string keys (names) stored in dictionary
# - Track member count for each group's root
# - When unioning, combine member counts
# - Print merged group size after each union


parent = dict()
ranks = dict()
members = dict()


def make_set():
    global parent, ranks, members
    parent = dict()
    ranks = dict()
    members = dict()


def find_set(u):
    if parent.get(u) is not None and parent[u] is not u:
        parent[u] = find_set(parent[u])
    else:
        parent[u] = u
    return parent[u]


def union_set(u, v):
    up = find_set(u)
    vp = find_set(v)
    if ranks.get(up) is None:
        ranks[up] = 1
    if ranks.get(vp) is None:
        ranks[vp] = 1
    if members.get(up) is None:
        members[up] = 1
    if members.get(vp) is None:
        members[vp] = 1

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
        F = int(input())

        make_set()
        for i in range(F):
            u, v = map(str, input().split())
            current_members = union_set(u, v)
            print(current_members)


solution()
