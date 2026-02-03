# Problem from Codeforces
# http://codeforces.com/problemset/problem/468/B
#
# Problem: Two Sets
#
# Description:
# Given n integers and two values a and b, partition the integers into two
# sets A and B such that:
# - For every x in set A, (a - x) must also be in set A
# - For every x in set B, (b - x) must also be in set B
# Determine if such a partition is possible.
#
# Input:
# - First line: n, a, b
# - Second line: n distinct integers
#
# Output:
# - "YES" followed by n lines (0 for set B, 1 for set A), or "NO"
#
# Approach:
# - Use DSU to create constraints between numbers
# - If x exists but (a-x) doesn't, x must go to set B (union with B marker)
# - If x exists but (b-x) doesn't, x must go to set A (union with A marker)
# - If both exist, union x with both complements
# - Check if A and B markers end up in same set (impossible)


parent = []
ranks = []


def make_set(N):
    global parent, ranks
    parent = [i for i in range(N + 5)]
    ranks = [0 for i in range(N + 5)]


def find_set(u):
    if parent[u] != u:
        parent[u] = find_set(parent[u])
    else:
        parent[u] = u
    return parent[u]


def union_set(u, v):
    up = find_set(u)
    vp = find_set(v)

    if ranks[up] > ranks[vp]:
        parent[vp] = up
    elif ranks[up] < ranks[vp]:
        parent[up] = vp
    else:
        parent[up] = vp
        ranks[vp] += 1


def solution():
    set_indicators = dict()
    n, a, b = map(int, input().split())
    numbers = list(map(int, input().split()))
    A = n + 1
    B = A + 1

    make_set(n)
    for i in range(n):
        set_indicators[numbers[i]] = i

    for i in range(n):
        if set_indicators.get(a - numbers[i]) is not None:
            union_set(i, set_indicators.get(a - numbers[i]))
        else:
            union_set(i, B)
        if set_indicators.get(b - numbers[i]) is not None:
            union_set(i, set_indicators.get(b - numbers[i]))
        else:
            union_set(i, A)
    if find_set(A) == find_set(B):
        print('NO')
        return

    print('YES')
    for i in range(n):
        print(1 if find_set(i) == find_set(n + 2) else 0)


solution()
