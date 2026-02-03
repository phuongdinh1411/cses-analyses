# BLUE_LEC18P02
"""
Problem: Spiral Matrix Coordinates (Ant on a Chessboard / Diagonal Walk)

Description:
Imagine an infinite grid where cells are numbered starting from (1,1) in a diagonal
spiral pattern. Given a cell number, find its (x, y) coordinates.

The pattern follows a diagonal spiral:
- Start at (1,1) = cell 1
- Move diagonally, filling cells in a pattern where perfect squares mark corners
- Odd perfect squares are at (k,1), even perfect squares are at (1,k)

For example:
  Cell 1 -> (1,1)
  Cell 2 -> (2,1)
  Cell 3 -> (1,2)
  Cell 4 -> (2,2)
  Cell 5 -> (1,3)
  ...

Input Format:
- Line 1: Integer T (number of test cases)
- Next T lines: Each contains a single integer representing the cell number

Output Format:
- For each test case: "Case X: x y" where (x, y) are the coordinates

Algorithm/Approach:
1. Find the smallest perfect square >= given number: sqrt = ceil(sqrt(n))
2. Calculate remainder r = sqrt^2 - n
3. Determine position based on remainder and whether sqrt is odd/even:
   - If r < sqrt: coordinates are (sqrt, r+1) or (r+1, sqrt)
   - Otherwise: calculate offset from the corner
4. Swap x,y if sqrt is odd (alternating diagonal directions)
"""
import math


def solution():
    T = int(input())

    for i in range(T):
        second = int(input())

        sqrt = math.ceil(math.sqrt(second))
        r = sqrt * sqrt - second
        if r < sqrt:
            y = r + 1
            x = sqrt
        else:
            x = 2 * sqrt - r - 1
            y = sqrt

        if sqrt % 2 == 1:
            x, y = y, x

        print("Case {0}: {1} {2}".format(i + 1, x, y))


solution()
