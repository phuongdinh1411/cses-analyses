# The Boggle Game

## Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

## Problem Statement

In the PigEwu language, each word has exactly 4 letters and contains exactly 2 vowels (A, E, I, O, U, Y).

In Boggle, you have a 4×4 grid of letters. A word is a sequence of 4 distinct adjacent squares (sharing edge or corner) forming a legal PigEwu word.

Given two Boggle boards, find all PigEwu words common to both boards.

## Input Format
- Pairs of 4×4 boards (same row of both boards on same line, separated by 4 spaces)
- Board pairs separated by blank line
- Input terminated by '#'

## Output Format
For each pair, output alphabetically sorted common words, or "There are no common words for this pair of boggle boards."

## Solution

### Approach
1. For each board, use DFS/backtracking to find all valid 4-letter words with exactly 2 vowels
2. Start DFS from each cell, exploring all 8 directions
3. Track visited cells to ensure distinct squares
4. Find intersection of words from both boards

### Python Solution

```python
def solve():
  VOWELS = set('AEIOUY')
  DIRS = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

  def count_vowels(word):
    return sum(1 for c in word if c in VOWELS)

  def find_words(board):
    words = set()
    visited = [[False] * 4 for _ in range(4)]

    def dfs(r, c, path):
      if len(path) == 4:
        if count_vowels(path) == 2:
          words.add(path)
        return

      visited[r][c] = True

      for dr, dc in DIRS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 4 and 0 <= nc < 4 and not visited[nr][nc]:
          dfs(nr, nc, path + board[nr][nc])

      visited[r][c] = False

    for i in range(4):
      for j in range(4):
        dfs(i, j, board[i][j])

    return words

  first = True

  while True:
    # Read two boards
    boards = [[], []]

    try:
      for row in range(4):
        line = input()
        if line.strip() == '#':
          return

        parts = line.split()
        if len(parts) >= 8:
          boards[0].append([parts[i] for i in range(4)])
          boards[1].append([parts[i] for i in range(4, 8)])
    except EOFError:
      return

    if not first:
      print()
    first = False

    # Find words in both boards
    words1 = find_words(boards[0])
    words2 = find_words(boards[1])

    # Find common words
    common = sorted(words1 & words2)

    if common:
      for word in common:
        print(word)
    else:
      print("There are no common words for this pair of boggle boards.")

    # Read blank line between test cases
    try:
      input()
    except:
      pass

if __name__ == "__main__":
  solve()
```

### Alternative Solution

```python
def solve():
  VOWELS = "AEIOUY"

  def is_valid_word(word):
    return len(word) == 4 and sum(c in VOWELS for c in word) == 2

  def get_all_words(board):
    words = set()
    directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

    def backtrack(r, c, path, visited):
      if len(path) == 4:
        if is_valid_word(path):
          words.add(path)
        return

      for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 4 and 0 <= nc < 4 and (nr, nc) not in visited:
          visited.add((nr, nc))
          backtrack(nr, nc, path + board[nr][nc], visited)
          visited.remove((nr, nc))

    for i in range(4):
      for j in range(4):
        backtrack(i, j, board[i][j], {(i, j)})

    return words

  import sys
  lines = sys.stdin.read().strip().split('\n')
  idx = 0
  first_case = True

  while idx < len(lines):
    if lines[idx].strip() == '#':
      break

    # Read 4 rows for both boards
    board1, board2 = [], []
    for _ in range(4):
      parts = lines[idx].split()
      board1.append(parts[:4])
      board2.append(parts[4:])
      idx += 1

    if not first_case:
      print()
    first_case = False

    words1 = get_all_words(board1)
    words2 = get_all_words(board2)
    common = sorted(words1 & words2)

    if common:
      print('\n'.join(common))
    else:
      print("There are no common words for this pair of boggle boards.")

    # Skip blank line
    if idx < len(lines) and lines[idx].strip() == '':
      idx += 1

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(4 × 4 × 8^3) = O(2048) per board for DFS exploration
- **Space Complexity:** O(W) where W is number of unique words found

### Key Insight
Use backtracking to explore all valid paths of length 4 from each starting cell. The constraint of exactly 2 vowels filters the valid PigEwu words. Finding common words is a simple set intersection.
