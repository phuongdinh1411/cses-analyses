# Problem from UVA
# https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1415
#
# Problem Name: Where is the Marble? (UVA 10474)
#
# Problem Description:
# Given N marbles with numbers written on them, sort them and answer Q queries.
# Each query asks for the position of a marble with a specific number.
#
# Input Format:
# - Multiple test cases until N=0 and Q=0
# - For each test case:
#   - N Q: number of marbles, number of queries
#   - N marble values (one per line)
#   - Q query values (one per line)
#
# Output Format:
# - "CASE# X:" followed by query results
#   - "Q found at P" if found (1-indexed position)
#   - "Q not found" if not present
#
# Key Approach/Algorithm:
# - Sort the marbles
# - For each query, use binary search (bisect_left) to find position
# - Check if the found position contains the query value
# import sys
import bisect

INF = float(1e9)
# sys.stdout = open("file.txt", "w+")


def solution():
    case = 1
    while True:
        N, Q = map(int, input().strip().split())

        if N == 0:
            break

        marbles = []
        for i in range(N):
            marbles.append(int(input().strip()))

        # sorted(marbles)
        marbles.sort()

        print('CASE# ' + str(case) + ':')
        for i in range(Q):
            q = int(input().strip())
            result = bisect.bisect_left(marbles, q)

            if 0 <= result < len(marbles) and marbles[result] == q:
                print('{:d} found at {:d}'.format(q, result + 1))
            else:
                print('{:d} not found'.format(q))

        case += 1


solution()


