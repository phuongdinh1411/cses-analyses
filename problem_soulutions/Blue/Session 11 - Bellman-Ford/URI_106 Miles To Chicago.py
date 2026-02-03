# Problem from URI
# https://www.urionlinejudge.com.br/judge/en/problems/view/1655
#
# Problem Name: 106 Miles To Chicago
#
# Problem Description:
# A spy needs to travel from intersection 1 to intersection n through Chicago.
# Each road segment has a probability of not being spotted (given as percentage).
# Find the maximum probability of traveling the entire path without being spotted.
# The total probability is the product of individual segment probabilities.
#
# Input Format:
# - Multiple test cases until n=0
# - For each test case:
#   - n m: number of intersections and streets
#   - m lines with a b p: street between a and b with p% probability of not being spotted
#
# Output Format:
# - Maximum probability (as percentage) of reaching n from 1 unspotted
#
# Key Approach/Algorithm:
# - Modified Bellman-Ford to maximize product of probabilities
# - Initialize source with 100% probability
# - Relax edges by multiplying probabilities instead of adding distances
# - Edges are bidirectional

import sys


class input_tokenizer:
    __tokens = None

    def has_next(self):
        return self.__tokens != [] and self.__tokens != None

    def next(self):
        token = self.__tokens[-1]
        self.__tokens.pop()
        return token

    def __init__(self):
        self.__tokens = sys.stdin.read().split()[::-1]


inp = input_tokenizer()


INF = -int(1e9)


def bellman_ford(n, m, E):
    dist = [INF for i in range(n + 1)]
    dist[1] = 100
    for i in range(1, n):
        for j in range(m):
            u = E[j][0]
            v = E[j][1]
            w = E[j][2]
            if dist[u] != INF and dist[u] * w / 100 > dist[v]:
                dist[v] = dist[u] * w / 100

    return "{:.6f}".format(dist[n]) + ' percent'


def solution():
    while True:
        n = int(inp.next())
        if n == 0:
            break
        m = int(inp.next())

        E = []
        for i in range(m):
            a = int(inp.next())
            b = int(inp.next())
            p = int(inp.next())
            E.append([a, b, p])
            E.append([b, a, p])

        print(bellman_ford(n, m * 2, E))


solution()


