# Problem from Codeforces
# http://codeforces.com/problemset/problem/540/C
#
# Problem: Ice Cave
#
# You're in an ice cave represented as an n×m grid. Each cell is either:
# - '.' (intact ice) - you can step on it, but it will crack and become 'X'
# - 'X' (cracked ice) - you cannot step on it; stepping on it means falling through
#
# You start at position (r1, c1) and want to reach (r2, c2). The goal is to
# FALL THROUGH the ice at the destination (the destination must become cracked
# when you step on it).
#
# You can reach the destination if:
# - There's a valid path from start to an adjacent cell of destination
# - The destination ice will crack when you step on it (either already cracked,
#   or you've visited an adjacent cell that cracks it)
#
# Input:
# - Line 1: n m (grid dimensions)
# - Next n lines: Grid of '.' and 'X'
# - Line n+2: r1 c1 (starting position, 1-indexed)
# - Line n+3: r2 c2 (destination position, 1-indexed)
#
# Output: "YES" if you can reach and fall through at destination, "NO" otherwise
#
# Approach: BFS pathfinding with special handling for destination cell


import queue


def can_reach_destination(starting_point, ending_point, n, m, matrix):
    dx = [1, 0, -1, 0]
    dy = [0, -1, 0, 1]

    visited = [[False for i in range(m)] for j in range(n)]

    visited[starting_point[0]][starting_point[1]] = True

    q = queue.Queue()
    q.put(starting_point)
    while not q.empty():
        checking_node = q.get()
        for l in range(4):
            neighbor_x = checking_node[0] + dx[l]
            neighbor_y = checking_node[1] + dy[l]
            if neighbor_x == ending_point[0] and neighbor_y == ending_point[1]:
                if matrix[neighbor_x][neighbor_y] == 'X':
                    return 'YES'
                else:
                    for end_check in range(4):
                        end_neighbor_x = neighbor_x + dx[end_check]
                        end_neighbor_y = neighbor_y + dy[end_check]
                        if 0 <= end_neighbor_x < n and 0 <= end_neighbor_y < m and matrix[end_neighbor_x][end_neighbor_y] == '.':
                            if end_neighbor_x != checking_node[0] or end_neighbor_y != checking_node[1]:
                                return 'YES'
                    return 'NO'
            else:
                if 0 <= neighbor_x < n and 0 <= neighbor_y < m and matrix[neighbor_x][neighbor_y] == '.' and not visited[neighbor_x][neighbor_y]:
                    q.put([neighbor_x, neighbor_y])
                    visited[neighbor_x][neighbor_y] = True

    return 'NO'


def solution():
    n, m = map(int, input().split())
    matrix = []
    for i in range(n):
        matrix.append(input().strip())

    starting_point = list(map(int, input().split()))
    ending_point = list(map(int, input().split()))

    starting_point[0] -= 1
    starting_point[1] -= 1
    ending_point[0] -= 1
    ending_point[1] -= 1

    print(can_reach_destination(starting_point, ending_point, n, m, matrix))


solution()


