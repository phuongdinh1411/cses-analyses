# Cipher

## Problem Information
- **Source:** HackerRank
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

Jack and Daniel encrypt messages using a cipher. A message b is encoded by writing it k times (shifted by 0, 1, ..., k-1 positions) and XORing all columns together.

Given encoded string s and parameter k, decode the original message.

Example: b = 1001011, k = 4
```
1001011      shift 0
01001011     shift 1
001001011    shift 2
0001001011   shift 3
----------
1110101001   XORed result s
```

## Input Format
- First line: n and k (length of original, number of shifts)
- Second line: encoded string s of length n + k - 1

## Constraints
- 1 ≤ n ≤ 10⁶
- 1 ≤ k ≤ 10⁶

## Output Format
Decoded message of length n.

## Example
```
Input:
7 4
1110100110

Output:
1001011
```
Original message b="1001011" with k=4. Encoding creates string of length n+k-1=10. Decoding "1110100110" with k=4 recovers the original "1001011".

## Solution

### Approach
For each position i in the encoded string s:
- s[i] = XOR of b[i], b[i-1], ..., b[i-k+1] (for valid indices)

We can decode left to right:
- b[0] = s[0]
- For i ≥ 1: b[i] = s[i] XOR b[i-1] XOR b[i-2] XOR ... (up to k-1 previous bits)

Use a running XOR of the last min(k, i+1) bits of b.

### Python Solution

```python
def solve():
  n, k = map(int, input().split())
  s = input().strip()

  b = []
  xor_sum = 0  # Running XOR of last k bits of b

  for i in range(n):
    # s[i] = xor of b[max(0,i-k+1)] to b[i]
    # So b[i] = s[i] XOR (xor of b[max(0,i-k+1)] to b[i-1])
    # The "xor of previous" is our running xor_sum

    bit = int(s[i]) ^ xor_sum
    b.append(str(bit))

    # Update running XOR
    xor_sum ^= bit

    # Remove contribution of b[i-k+1] if it exists (sliding window)
    if i >= k - 1:
      xor_sum ^= int(b[i - k + 1])

  print(''.join(b))

if __name__ == "__main__":
  solve()
```

### Alternative Solution

```python
def solve():
  n, k = map(int, input().split())
  s = input().strip()

  result = []
  window_xor = 0

  for i, char in enumerate(s[:n]):  # Use enumerate for cleaner iteration
    # Decode b[i]
    # s[i] = window_xor ^ b[i], so b[i] = s[i] ^ window_xor
    b_i = int(char) ^ window_xor
    result.append(b_i)

    # Add b[i] to window
    window_xor ^= b_i

    # Remove b[i-k+1] from window if window exceeds k
    if i >= k - 1:
      window_xor ^= result[i - k + 1]

  print(''.join(map(str, result)))

if __name__ == "__main__":
  solve()
```

### One-liner Style

```python
def solve():
  n, k = map(int, input().split())
  s = input().strip()

  b = [0] * n
  xor = 0

  for i in range(n):
    b[i] = int(s[i]) ^ xor
    xor ^= b[i]
    if i >= k - 1:
      xor ^= b[i - k + 1]

  print(''.join(map(str, b)))

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(N)
- **Space Complexity:** O(N)

### Key Insight
The encoded string at position i is the XOR of a window of k bits from the original. By maintaining a sliding window XOR, we can decode each bit in O(1) time. When the window slides past position k, we XOR out the oldest bit.
