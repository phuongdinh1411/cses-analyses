# Problem from UVA
# https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=1498
#
# Problem Name: XYZZY (UVA 10557)
#
# Problem Description:
# A text adventure game where the player starts in room 1 with 100 energy.
# Moving to a room adds/subtracts energy based on the room's energy value.
# The player dies if energy drops to 0 or below. Determine if the player
# can reach the last room (room n) with positive energy.
#
# Input Format:
# - Multiple test cases until n=-1
# - For each test case:
#   - n: number of rooms
#   - For each room: energy_value, num_connections, connected_rooms...
#
# Output Format:
# - "winnable" if player can reach room n with positive energy, "hopeless" otherwise
#
# Key Approach/Algorithm:
# - Modified Bellman-Ford to maximize energy (find longest path)
# - Only traverse edges if current energy > 0
# - If a positive cycle exists that can reach room n, game is winnable
# - Detect positive cycles that allow infinite energy gain

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


INF = int(1e9)


def bellman_ford(N, M, E):
    dist = [-INF for i in range(N)]

    dist[0] = 100
    for i in range(0, N-1):
        for j in range(M):
            u = E[j][0]
            v = E[j][1]
            w = E[j][2]
            if dist[u] != -INF and dist[u] + w > dist[v] and dist[u] + w > 0:
                dist[v] = dist[u] + w
    for j in range(M):
        u = E[j][0]
        v = E[j][1]
        w = E[j][2]
        if dist[u] != -INF and dist[u] + w > dist[v] != -INF:
            return 'winnable'

    return 'hopeless' if dist[N - 1] < 0 else 'winnable'


def solution():
    while True:
        N = int(inp.next())
        if N == -1:
            break
        E = []
        energies = []
        for i in range(N):
            energy = int(inp.next())
            energies.append(energy)
            connections = int(inp.next())
            for j in range(connections):
                neighbor = int(inp.next()) - 1
                E.append([i, neighbor])
        for connection in E:
            connection.append(energies[connection[1]])
        print(bellman_ford(N, len(E), E))


solution()


