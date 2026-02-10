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
# - We need to reach an adjacent cell of destination
# - If destination is 'X', we just need to reach any adjacent cell
# - If destination is '.', we need to reach it from an adjacent cell,
#   AND there must be another intact adjacent cell (so destination cracks when we step on it)


from collections import deque


def can_reach_destination(start, end, n, m, matrix):
    dx = [1, 0, -1, 0]
    dy = [0, -1, 0, 1]

    # Special case: start == end
    if start == end:
        # We start here, the cell cracks. We need to step on it again to fall through.
        # Count intact neighbors we can go to and come back from
        intact_neighbors = 0
        for i in range(4):
            nx, ny = start[0] + dx[i], start[1] + dy[i]
            if 0 <= nx < n and 0 <= ny < m and matrix[nx][ny] == '.':
                intact_neighbors += 1
        # Need at least 2 intact neighbors: one to go to, one to come back from
        # (or same neighbor, but we need the destination to be cracked when we return)
        # Actually, we need at least 1 neighbor to go to, and when we return,
        # the start cell is now cracked. So we just need 1 intact neighbor.
        # Wait, re-reading: if start==end and destination is '.', we step on it (cracks),
        # go somewhere, come back and fall through. But when we step initially, it cracks.
        # To come back, we need to reach it again from an adjacent cell.
        # So we need at least 1 intact neighbor to go to, and 1 neighbor (can be same or different)
        # to return from. Since we can only visit intact cells, we need at least 1 intact neighbor
        # to leave, and the cell is cracked when we return.
        return 'YES' if intact_neighbors >= 1 else 'NO'

    visited = [[False] * m for _ in range(n)]
    visited[start[0]][start[1]] = True

    q = deque()
    q.append(start)

    # Track if we can reach the destination successfully
    can_fall = False

    while q:
        curr = q.popleft()

        for i in range(4):
            nx, ny = curr[0] + dx[i], curr[1] + dy[i]

            if not (0 <= nx < n and 0 <= ny < m):
                continue

            if nx == end[0] and ny == end[1]:
                # We're adjacent to the destination
                if matrix[nx][ny] == 'X':
                    # Destination is already cracked, we can fall through
                    return 'YES'
                else:
                    # Destination is intact ('.')
                    # We need another intact cell adjacent to destination
                    # (besides the current cell we're standing on)
                    # so that when we step on destination, it cracks, and we fall
                    # Actually, the destination cracks when we step on it.
                    # The question is: can we step on it? Yes, if we can reach an adjacent cell.
                    # When we step on it from curr, it becomes cracked and we fall.
                    # BUT we also need to be able to reach curr first!
                    # The current cell 'curr' was intact when we visited it, now it's cracked.
                    # We need to check if there's another adjacent intact cell to destination.
                    for j in range(4):
                        adjx, adjy = nx + dx[j], ny + dy[j]
                        if 0 <= adjx < n and 0 <= adjy < m:
                            if adjx == curr[0] and adjy == curr[1]:
                                continue  # Skip the cell we came from
                            if matrix[adjx][adjy] == '.':
                                # There's another intact cell adjacent to destination
                                # We step from curr to destination, it cracks, we fall
                                # But wait: the destination being '.' means when we step on it,
                                # it becomes 'X'. But we want to FALL through.
                                # To fall, the cell must be 'X' when we step on it.
                                # So if destination is '.', we need to crack it first, then step again.
                                # That means we need to visit destination, leave to another cell,
                                # then return to destination (now cracked).
                                # So we need: path to dest's neighbor A, then dest (cracks),
                                # then another neighbor B of dest (must be intact), then back to dest.
                                # This simplifies to: destination must have >= 2 adjacent intact cells
                                # that we can reach.
                                can_fall = True
                                break
                    if can_fall:
                        return 'YES'
            elif matrix[nx][ny] == '.' and not visited[nx][ny]:
                visited[nx][ny] = True
                q.append([nx, ny])

    return 'NO'


def solution():
    n, m = map(int, input().split())
    matrix = []
    for _ in range(n):
        matrix.append(input().strip())

    start = list(map(int, input().split()))
    end = list(map(int, input().split()))

    # Convert to 0-indexed
    start[0] -= 1
    start[1] -= 1
    end[0] -= 1
    end[1] -= 1

    print(can_reach_destination(start, end, n, m, matrix))


solution()
