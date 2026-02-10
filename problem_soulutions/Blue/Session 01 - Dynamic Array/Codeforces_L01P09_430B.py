# Problem from Codeforces
# http://codeforces.com/problemset/problem/430/B
#
# Problem: Balls Game
#
# A row of n colored balls is arranged in a line. You have one ball of color x
# that you can insert anywhere in the row. When k or more consecutive balls of
# the same color form, they are destroyed. Chain reactions can occur.
# Find the maximum number of balls you can destroy.
#
# Input:
# - Line 1: n k x (number of balls, threshold for destruction, your ball's color)
# - Line 2: n integers (colors of balls in the row)
#
# Output: Maximum number of balls that can be destroyed
#
# Approach:
# 1. Find all runs (consecutive sequences) of balls
# 2. For each run of color x, calculate what happens if we add one ball to it
# 3. Simulate chain reactions by checking adjacent runs
# Time complexity: O(n)


def get_runs(colors):
    """Convert array to list of (color, count) tuples representing consecutive runs."""
    if not colors:
        return []
    runs = []
    current_color = colors[0]
    count = 1
    for i in range(1, len(colors)):
        if colors[i] == current_color:
            count += 1
        else:
            runs.append((current_color, count))
            current_color = colors[i]
            count = 1
    runs.append((current_color, count))
    return runs


def simulate_destruction(runs, run_index, k):
    """
    Simulate inserting a ball into run at run_index and count total destroyed.
    The run at run_index has color x, and we're adding 1 ball to it.
    """
    destroyed = 0
    left = run_index
    right = run_index

    # Initial run gets +1 ball from our insertion
    current_count = runs[run_index][1] + 1

    # Check if we can destroy
    if current_count < k:
        return 0

    # Destroy and chain react
    while True:
        if current_count >= k:
            destroyed += current_count
            left -= 1
            right += 1

            # Check if adjacent runs have the same color and can merge
            if left >= 0 and right < len(runs) and runs[left][0] == runs[right][0]:
                current_count = runs[left][1] + runs[right][1]
                # Continue with merged run
            else:
                break
        else:
            break

    return destroyed


n, k, x = map(int, input().split())
c = list(map(int, input().split()))

# Get all runs of consecutive colors
runs = get_runs(c)

max_destroyed = 0

# Try inserting our ball into each run of color x
for i, (color, count) in enumerate(runs):
    if color == x:
        destroyed = simulate_destruction(runs, i, k)
        max_destroyed = max(max_destroyed, destroyed)

print(max_destroyed)
