#  Problem from Light OJ
#  http://lightoj.com/volume_showproblem.php?problem=1012
#
# Problem: Guilty Prince
#
# A prince is standing in a dungeon cell. The dungeon is a W×H grid where:
# - '.' represents an empty cell (passable)
# - '#' represents a wall (impassable)
# - '@' represents the prince's starting position (also passable)
#
# The prince can move in 4 directions (up, down, left, right). Count the
# total number of cells the prince can reach from his starting position.
#
# Input:
# - Line 1: T (number of test cases)
# - For each test case:
#   - Line 1: W H (width and height of dungeon)
#   - Next H lines: The dungeon grid
#
# Output: For each test case, print "Case X: Y" where Y is the count of
#         reachable cells (including the starting cell)
#
# Approach: BFS flood fill from prince's position


from collections import deque


def calculate_possible_cells(width, height, matrix, prince_position):
    dx = [1, 0, -1, 0]
    dy = [0, -1, 0, 1]

    visited = [[False for _ in range(width)] for _ in range(height)]
    q = deque()
    q.append(prince_position)

    # Fixed: Mark starting position as visited
    visited[prince_position[0]][prince_position[1]] = True
    total_possible_cells = 1

    while q:
        checking_node = q.popleft()
        for i in range(4):
            neighbor_x = checking_node[0] + dx[i]
            neighbor_y = checking_node[1] + dy[i]
            if (0 <= neighbor_x < height and
                0 <= neighbor_y < width and
                matrix[neighbor_x][neighbor_y] in '.@' and
                not visited[neighbor_x][neighbor_y]):
                q.append([neighbor_x, neighbor_y])
                visited[neighbor_x][neighbor_y] = True
                total_possible_cells += 1

    return total_possible_cells


def solution():
    results = []
    T = int(input())
    for i in range(T):
        Wi, Hi = map(int, input().split())
        matrix = []
        prince_position = []
        for j in range(Hi):
            new_line = input().strip()
            if '@' in new_line:
                prince_position = [j, new_line.find('@')]
            matrix.append(new_line)
        results.append('Case {0}: {1}'.format(i + 1, calculate_possible_cells(Wi, Hi, matrix, prince_position)))

    print(*results, sep='\n')


solution()
