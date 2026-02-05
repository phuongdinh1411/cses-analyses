# Polo the Penguin and the XOR

## Problem Information
- **Source:** Codechef
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

Polo, the Penguin, likes the XOR operation.

XOR-sum of a list of numbers is the result of XOR-ing all of them. XOR-sum of (A₁ ⊕ A₂ ⊕ ... ⊕ Aₙ) is defined as A₁ ⊕ (A₂ ⊕ (A₃ ⊕ (... ⊕ Aₙ)))

He has an array A consisting of N integers. Index in the array are numbered from 1 to N, inclusive. Let us denote by F(L, R), the XOR-sum of all integers in the array A whose indices lie from L to R, inclusive, i.e. F(L, R) = A_L ⊕ A_{L+1} ⊕ ... ⊕ A_R.

Your task is to find the total sum of XOR-sums F(L, R) over all L and R, such that 1 ≤ L ≤ R ≤ N.

## Input Format
- First line: T denoting the number of test cases
- For each test case:
  - First line: N denoting the size of array
  - Second line: N space-separated integers A₁, A₂, ..., Aₙ

## Constraints
- 1 ≤ T ≤ 100,000
- 1 ≤ N ≤ 100,000
- 0 ≤ Aᵢ ≤ 1,000,000,000 (10⁹)
- The total sum of all N over all test cases will not exceed 100,000

## Output Format
For each test case, output a single line containing the total sum to the corresponding test case.

## Solution

### Approach
For each bit position, count how many subarrays have that bit set in their XOR.

Key insight: Use prefix XOR. Let `P[i] = A[1] ⊕ A[2] ⊕ ... ⊕ A[i]` (with P[0] = 0).
Then `F(L, R) = P[R] ⊕ P[L-1]`.

For a specific bit b:
- F(L,R) has bit b set if P[R] and P[L-1] differ at bit b
- Count pairs where one has bit b set and one doesn't

For each bit position:
- Count of prefix values with bit set: `ones`
- Count with bit unset: `zeros`
- Number of subarrays with bit set = `ones × zeros`
- Contribution to sum = `ones × zeros × 2^b`

### Python Solution

```python
def solve():
 t = int(input())

 for _ in range(t):
  n = int(input())
  arr = list(map(int, input().split()))

  # Compute prefix XOR
  prefix = [0] * (n + 1)
  for i in range(n):
   prefix[i + 1] = prefix[i] ^ arr[i]

  total_sum = 0

  # For each bit position (up to 30 bits for 10^9)
  for bit in range(30):
   mask = 1 << bit
   ones = 0
   zeros = 0

   # Count prefix values with this bit set/unset
   for i in range(n + 1):
    if prefix[i] & mask:
     ones += 1
    else:
     zeros += 1

   # Number of subarrays with this bit set in XOR
   # = pairs where P[R] and P[L-1] differ at this bit
   count = ones * zeros

   # Add contribution
   total_sum += count * mask

  print(total_sum)

if __name__ == "__main__":
 solve()
```

### Optimized Solution

```python
def solve():
 t = int(input())

 for _ in range(t):
  n = int(input())
  arr = list(map(int, input().split()))

  total_sum = 0
  prefix_xor = 0

  # For each bit, track count of 0s and 1s in prefix XOR
  bit_count = [[1, 0] for _ in range(30)]  # Initially prefix[0]=0

  for num in arr:
   prefix_xor ^= num

   for bit in range(30):
    mask = 1 << bit
    bit_val = (prefix_xor >> bit) & 1

    # Subarrays ending here with this bit set
    # = count of previous prefixes with opposite bit
    opposite = 1 - bit_val
    count = bit_count[bit][opposite]
    total_sum += count * mask

    # Update count
    bit_count[bit][bit_val] += 1

  print(total_sum)

if __name__ == "__main__":
 solve()
```

### Complexity Analysis
- **Time Complexity:** O(N × 30) = O(N) per test case
- **Space Complexity:** O(30) = O(1) for bit counts

### Key Insight
Using prefix XOR, `F(L,R) = P[R] ⊕ P[L-1]`. For each bit position, a subarray contributes `2^bit` to the sum if that bit is set in its XOR. This happens when P[R] and P[L-1] differ at that bit position. The total contribution of bit b is `(count_of_1s × count_of_0s) × 2^b`.
