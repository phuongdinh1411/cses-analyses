# Bit Maps

## Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

## Problem Statement

Convert between two bitmap representations:
1. **B format**: 2D array of 0s and 1s (row by row)
2. **D format**: Recursive decomposition where:
   - Output '1' if all bits are 1
   - Output '0' if all bits are 0
   - Output 'D' and recursively process 4 quarters (top-left, top-right, bottom-left, bottom-right)

When dividing:
- Odd columns: left quarters have one more column than right
- Odd rows: top quarters have one more row than bottom

## Input Format
- Format character (B or D), dimensions (rows, columns)
- The bitmap data (max 50 chars per line)
- Terminated by '#'

## Output Format
Convert each bitmap to the other format, with dimensions right-justified (width 4 for rows, 3 for columns).

## Solution

### Approach
- **B to D**: Recursively check if region is all 0s, all 1s, or mixed. Mixed regions output 'D' and recurse on quarters.
- **D to B**: Read characters and fill regions recursively based on '0', '1', or 'D'.

### Python Solution

```python
def solve():
  import sys
  data = sys.stdin.read().split()
  idx = 0

  while idx < len(data):
    fmt = data[idx]
    if fmt == '#':
      break

    h = int(data[idx + 1])
    w = int(data[idx + 2])
    idx += 3

    if fmt == 'B':
      # Read bitmap
      chars_needed = h * w
      bitmap_str = ""
      while len(bitmap_str) < chars_needed:
        bitmap_str += data[idx]
        idx += 1

      bitmap = [[0] * w for _ in range(h)]
      for i in range(h):
        for j in range(w):
          bitmap[i][j] = int(bitmap_str[i * w + j])

      # Convert B to D
      def b2d(r, c, height, width):
        if height == 0 or width == 0:
          return ""

        total = sum(bitmap[r + i][c + j]
             for i in range(height) for j in range(width))

        if total == 0:
          return "0"
        if total == height * width:
          return "1"

        # Divide into quarters
        h1, h2 = (height + 1) // 2, height // 2
        w1, w2 = (width + 1) // 2, width // 2

        return ("D" +
            b2d(r, c, h1, w1) +          # top-left
            b2d(r, c + w1, h1, w2) +     # top-right
            b2d(r + h1, c, h2, w1) +     # bottom-left
            b2d(r + h1, c + w1, h2, w2)) # bottom-right

      result = b2d(0, 0, h, w)
      print(f"D{h:4d}{w:4d}")
      for i in range(0, len(result), 50):
        print(result[i:i+50])

    else:  # fmt == 'D'
      # Read D format
      d_str = ""
      # Estimate characters needed (at most h*w for fully expanded)
      while idx < len(data) and data[idx] not in ['B', 'D', '#']:
        d_str += data[idx]
        idx += 1

      bitmap = [['0'] * w for _ in range(h)]
      d_idx = [0]

      def d2b(r, c, height, width):
        if height == 0 or width == 0:
          return

        ch = d_str[d_idx[0]]
        d_idx[0] += 1

        if ch == '0' or ch == '1':
          for i in range(height):
            for j in range(width):
              bitmap[r + i][c + j] = ch
        else:  # 'D'
          h1, h2 = (height + 1) // 2, height // 2
          w1, w2 = (width + 1) // 2, width // 2

          d2b(r, c, h1, w1)
          d2b(r, c + w1, h1, w2)
          d2b(r + h1, c, h2, w1)
          d2b(r + h1, c + w1, h2, w2)

      d2b(0, 0, h, w)
      result = ''.join(''.join(row) for row in bitmap)

      print(f"B{h:4d}{w:4d}")
      for i in range(0, len(result), 50):
        print(result[i:i+50])

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(H × W) for both conversions
- **Space Complexity:** O(H × W) for storing the bitmap

### Key Insight
This is a divide and conquer problem with quadtree-like structure:
- B→D: Check if region is uniform; if not, divide into 4 parts
- D→B: Recursively fill regions based on the encoded characters

The quarter division rule handles odd dimensions correctly by giving the extra row/column to top/left quarters.
