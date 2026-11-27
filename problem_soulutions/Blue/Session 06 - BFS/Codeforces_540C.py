# Problem from Codeforces
# http://codeforces.com/problemset/problem/540/C
#
# Problem: Ice Cave
#
# Grid of intact '.' and cracked 'X' ice. Moving onto '.' cracks it; moving onto
# 'X' means falling through. Start (r1, c1) is always 'X'. Can you fall through
# at (r2, c2)?
#
# Approach: BFS where cracking a cell doubles as marking it visited. Answer YES
# the moment we move onto an 'X' cell that is the target. O(n * m).


from collections import deque


def can_fall(n, m, grid, start, end):
    grid = [list(row) for row in grid]
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < n and 0 <= ny < m):
                continue
            if grid[nx][ny] == 'X':
                if (nx, ny) == end:
                    return 'YES'
                continue
            grid[nx][ny] = 'X'  # stepping on intact ice cracks it
            queue.append((nx, ny))
    return 'NO'


def solution():
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]
    r1, c1 = map(int, input().split())
    r2, c2 = map(int, input().split())
    print(can_fall(n, m, grid, (r1 - 1, c1 - 1), (r2 - 1, c2 - 1)))


solution()
