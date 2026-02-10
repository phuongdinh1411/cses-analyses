#  Problem from SPOJ
#  https://www.spoj.com/problems/KOZE/
#
# Problem: KOZE - Sheep
#
# A backyard is represented as an N×M grid with:
# - '#' - fence (impassable)
# - '.' - empty grass
# - 'k' - sheep
# - 'v' - wolf
#
# Wolves eat sheep unless they're in a fenced area (surrounded by fence on
# all sides, not touching the boundary). In a fenced area, if there are more
# sheep than wolves, the sheep survive; otherwise wolves survive.
# Outside fenced areas (connected to boundary), both survive.
#
# Count how many sheep and wolves survive.
#
# Input:
# - Line 1: N M (grid dimensions)
# - Next N lines: The backyard grid
#
# Output: Two integers - surviving sheep and wolves
#
# Approach: BFS to find connected components, check if each touches boundary


from collections import deque


def calc_survive(N, M, matrix):
    visited = [[False for _ in range(M)] for _ in range(N)]

    dx = [1, 0, -1, 0]
    dy = [0, -1, 0, 1]

    total_wolves = 0
    total_sheep = 0

    for row in range(N):
        for col in range(M):
            cell = matrix[row][col]
            if cell in '.kv' and not visited[row][col]:
                visited[row][col] = True
                q = deque()
                q.append([row, col])

                sheep_count = 1 if cell == 'k' else 0
                wolf_count = 1 if cell == 'v' else 0

                # Fixed: Check if starting cell is on boundary
                is_fenced = not (row == 0 or row == N - 1 or col == 0 or col == M - 1)

                while q:
                    curr = q.popleft()
                    for i in range(4):
                        nx = curr[0] + dx[i]
                        ny = curr[1] + dy[i]
                        if (0 <= nx < N and 0 <= ny < M and
                            matrix[nx][ny] in '.kv' and
                            not visited[nx][ny]):
                            q.append([nx, ny])
                            visited[nx][ny] = True
                            if matrix[nx][ny] == 'k':
                                sheep_count += 1
                            elif matrix[nx][ny] == 'v':
                                wolf_count += 1
                            # Check if this cell is on boundary
                            if nx == 0 or nx == N - 1 or ny == 0 or ny == M - 1:
                                is_fenced = False

                if is_fenced:
                    # In a fenced area: only the majority survives
                    if sheep_count > wolf_count:
                        total_sheep += sheep_count
                    else:
                        total_wolves += wolf_count
                else:
                    # Not fenced: both survive
                    total_sheep += sheep_count
                    total_wolves += wolf_count

    return [total_sheep, total_wolves]


def solution():
    while True:
        new_line = input().strip()
        if new_line:
            N, M = map(int, new_line.split())
            break
    backyard = []
    i = 0
    while i < N:
        new_line = input().strip()
        if new_line:
            backyard.append(new_line)
            i += 1

    print(*calc_survive(N, M, backyard), sep=' ')


solution()
