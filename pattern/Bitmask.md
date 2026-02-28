---
layout: simple
title: "Bitmask Techniques"
permalink: /pattern/bitmask
---

# Bitmask Techniques — Comprehensive Pattern Guide

---

## What Are Bitmask Techniques?

Bitmask techniques use binary representations and bitwise operations to efficiently solve problems involving:

1. **Subsets and combinations**: Representing sets as binary numbers
2. **State compression**: Encoding complex states in integers
3. **Fast set operations**: Using bitwise AND, OR, XOR for O(1) operations
4. **Dynamic programming**: Tracking "which elements have been processed"

**Key Idea**: An n-bit integer can represent a subset of n elements, where bit i indicates whether element i is included.

```
Example: Set {0, 1, 2, 3}, subset {0, 2, 3}
Binary: 1101 (reading right to left: positions 0, 2, 3 are set)
Decimal: 13

All subsets of {0, 1, 2}:
000 (0) = {}
001 (1) = {0}
010 (2) = {1}
011 (3) = {0, 1}
100 (4) = {2}
101 (5) = {0, 2}
110 (6) = {1, 2}
111 (7) = {0, 1, 2}
```

**When to use bitmask**: n ≤ 20-24 elements (2^20 ≈ 1 million states)

---

## Table of Contents

1. [Fundamental Bit Operations](#1-fundamental-bit-operations)
2. [Subset Enumeration Techniques](#2-subset-enumeration-techniques)
3. [Bitmask DP Patterns](#3-bitmask-dp-patterns)
4. [Advanced Bit Tricks](#4-advanced-bit-tricks)
5. [SOS (Sum Over Subsets) DP](#5-sos-sum-over-subsets-dp)
6. [Common Problem Templates](#6-common-problem-templates)
7. [Practice Problems](#7-practice-problems)

---

## 1. Fundamental Bit Operations

### Basic Operations

```python
# ============================================
# CHECK, SET, CLEAR, TOGGLE
# ============================================

mask = 0b10110  # Binary: 10110

# Check if bit n is set
def is_set(mask, n):
    return bool(mask & (1 << n))

# Set bit n to 1
def set_bit(mask, n):
    return mask | (1 << n)

# Clear bit n (set to 0)
def clear_bit(mask, n):
    return mask & ~(1 << n)

# Toggle bit n
def toggle_bit(mask, n):
    return mask ^ (1 << n)

# Example
n = 2
print(f"Is bit {n} set in {bin(mask)}? {is_set(mask, n)}")  # True
mask = clear_bit(mask, n)
print(f"After clearing bit {n}: {bin(mask)}")  # 0b10010
```

### Counting and Finding Bits

```python
# ============================================
# POPCOUNT, LOWEST BIT, TRAILING ZEROS
# ============================================

# Count number of set bits (popcount)
def popcount_builtin(mask):
    return bin(mask).count('1')

def popcount_kernighan(mask):
    """Brian Kernighan's algorithm - O(number of set bits)"""
    count = 0
    while mask:
        mask &= mask - 1  # Remove lowest set bit
        count += 1
    return count

# Get the lowest set bit
def lowest_bit(mask):
    return mask & -mask
    # Example: 10110 & -10110 = 00010

# Remove the lowest set bit
def remove_lowest_bit(mask):
    return mask & (mask - 1)
    # Example: 10110 → 10100

# Count trailing zeros (position of lowest set bit)
def count_trailing_zeros(mask):
    if mask == 0:
        return 32  # Or 64 for 64-bit
    return (mask & -mask).bit_length() - 1

# Position of rightmost set bit (1-indexed)
def rightmost_bit_position(mask):
    return (mask & -mask).bit_length()

# Examples
mask = 0b10110
print(f"Popcount: {popcount_builtin(mask)}")  # 3
print(f"Lowest bit: {bin(lowest_bit(mask))}")  # 0b10
print(f"Trailing zeros: {count_trailing_zeros(mask)}")  # 1
```

### Checking Properties

```python
# ============================================
# CHECKING BITMASK PROPERTIES
# ============================================

# Check if power of 2 (exactly one bit set)
def is_power_of_2(mask):
    return mask > 0 and (mask & (mask - 1)) == 0

# Check if two masks are disjoint (no common bits)
def are_disjoint(mask1, mask2):
    return (mask1 & mask2) == 0

# Check if mask1 is subset of mask2
def is_subset(mask1, mask2):
    return (mask1 & mask2) == mask1

# Get bits in mask1 but not in mask2
def difference(mask1, mask2):
    return mask1 & ~mask2

# Get all bits up to position n
def all_bits(n):
    return (1 << n) - 1
    # Example: n=5 → 0b11111 (31)

# Examples
print(is_power_of_2(8))  # True
print(is_power_of_2(6))  # False
print(are_disjoint(0b1100, 0b0011))  # True
print(is_subset(0b0101, 0b1101))  # True
```

---

## 2. Subset Enumeration Techniques

### Iterate All Subsets

```python
# ============================================
# ENUMERATE ALL 2^n SUBSETS
# ============================================

def enumerate_all_subsets(n):
    """Generate all subsets of {0, 1, ..., n-1}"""
    for mask in range(1 << n):
        subset = [i for i in range(n) if mask & (1 << i)]
        yield mask, subset

# Example: All subsets of {0, 1, 2}
for mask, subset in enumerate_all_subsets(3):
    print(f"{mask:03b} → {subset}")

# Output:
# 000 → []
# 001 → [0]
# 010 → [1]
# 011 → [0, 1]
# 100 → [2]
# 101 → [0, 2]
# 110 → [1, 2]
# 111 → [0, 1, 2]
```

### Iterate All Submasks

```python
# ============================================
# ENUMERATE ALL SUBMASKS OF A MASK
# ============================================

def enumerate_submasks(mask):
    """
    Generate all submasks of mask in descending order.

    Key technique: submask = (submask - 1) & mask
    Time: O(2^k) where k = popcount(mask)
    """
    submask = mask
    while submask > 0:
        yield submask
        submask = (submask - 1) & mask

# Example: Submasks of 0b1011 (11)
mask = 0b1011
print(f"Submasks of {bin(mask)}:")
for submask in enumerate_submasks(mask):
    print(f"  {submask:04b} ({submask})")

# Output:
# Submasks of 0b1011:
#   1011 (11)
#   1010 (10)
#   1001 (9)
#   1000 (8)
#   0011 (3)
#   0010 (2)
#   0001 (1)

# Including empty submask
def enumerate_submasks_with_zero(mask):
    """Include the empty submask (0)"""
    submask = mask
    while True:
        yield submask
        if submask == 0:
            break
        submask = (submask - 1) & mask
```

### Iterate All Submask Pairs

```python
# ============================================
# ENUMERATE ALL WAYS TO PARTITION A MASK
# ============================================

def enumerate_submask_pairs(mask):
    """
    Generate all ways to partition mask into two non-empty parts.
    Returns (submask, complement) pairs.
    """
    submask = mask
    while submask > 0:
        complement = mask ^ submask  # mask XOR submask
        if complement > 0:  # Both must be non-empty
            yield (submask, complement)
        submask = (submask - 1) & mask

# Optimization: Avoid duplicate pairs
def enumerate_unique_submask_pairs(mask):
    """Generate unique pairs where submask <= complement"""
    submask = mask
    while submask > 0:
        complement = mask ^ submask
        if submask <= complement and complement > 0:
            yield (submask, complement)
        submask = (submask - 1) & mask

# Example: Partition 0b111 (7)
mask = 0b111
print("All partitions:")
for s1, s2 in enumerate_unique_submask_pairs(mask):
    print(f"  {s1:03b} | {s2:03b}")

# Output:
#   001 | 110
#   010 | 101
#   011 | 100
```

### Iterate k-Element Subsets (Gosper's Hack)

```python
# ============================================
# ENUMERATE ALL k-ELEMENT SUBSETS
# ============================================

def next_combination(mask):
    """
    Get next mask with same number of bits set.
    Gosper's hack - generates combinations in lexicographic order.
    """
    c = mask & -mask  # Rightmost set bit
    r = mask + c      # Add it
    return (((r ^ mask) >> 2) // c) | r

def enumerate_k_subsets(n, k):
    """Generate all C(n, k) subsets of size k from {0, 1, ..., n-1}"""
    if k == 0:
        yield 0
        return

    mask = (1 << k) - 1  # Start with k rightmost bits set
    limit = 1 << n

    while mask < limit:
        yield mask
        mask = next_combination(mask)

# Example: All 3-element subsets of 5 elements
print("All 3-element subsets of {0,1,2,3,4}:")
for mask in enumerate_k_subsets(5, 3):
    elements = [i for i in range(5) if mask & (1 << i)]
    print(f"  {mask:05b} → {elements}")

# Output:
#   00111 → [0, 1, 2]
#   01011 → [0, 1, 3]
#   01101 → [0, 2, 3]
#   01110 → [1, 2, 3]
#   10011 → [0, 1, 4]
#   ... (total of C(5,3) = 10 subsets)
```

---

## 3. Bitmask DP Patterns

### Pattern 1: Traveling Salesman Problem (TSP)

**Problem**: Visit all n cities exactly once, minimize total distance.

**State**: `dp[mask][i]` = minimum cost to visit cities in `mask`, ending at city `i`

```python
def tsp(dist, n):
    """
    Traveling Salesman Problem using bitmask DP.

    State: dp[mask][i] = min cost to visit cities in mask, ending at city i
    Transition: Try going from city i to unvisited city j

    Time: O(2^n * n^2)
    Space: O(2^n * n)
    """
    INF = float('inf')
    # dp[mask][i] = min cost to reach state (mask, i)
    dp = [[INF] * n for _ in range(1 << n)]

    # Base case: start at city 0
    dp[1][0] = 0

    # Fill DP table
    for mask in range(1 << n):
        for u in range(n):
            # Skip if city u not in mask or unreachable
            if not (mask & (1 << u)) or dp[mask][u] == INF:
                continue

            # Try going to unvisited city v
            for v in range(n):
                if mask & (1 << v):  # v already visited
                    continue

                next_mask = mask | (1 << v)
                dp[next_mask][v] = min(dp[next_mask][v],
                                      dp[mask][u] + dist[u][v])

    # Return minimum cost ending at any city (or add return to start)
    full_mask = (1 << n) - 1
    return min(dp[full_mask][i] for i in range(n))

# Example usage
dist = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]
print(f"Minimum TSP cost: {tsp(dist, 4)}")
```

### Pattern 2: Assignment Problem

**Problem**: Assign n workers to n jobs, minimize total cost.

**State**: `dp[mask]` = minimum cost to assign workers in `mask` to first k jobs

```python
def min_cost_assignment(cost, n):
    """
    Assign n workers to n jobs to minimize cost.

    State: dp[mask] = min cost to assign workers in mask to jobs 0..k-1
           where k = popcount(mask)

    Time: O(2^n * n)
    Space: O(2^n)
    """
    INF = float('inf')
    dp = [INF] * (1 << n)
    dp[0] = 0

    for mask in range(1 << n):
        if dp[mask] == INF:
            continue

        # Number of jobs already assigned
        jobs_assigned = bin(mask).count('1')

        # Try assigning next job to each unassigned worker
        for worker in range(n):
            if mask & (1 << worker):  # Worker already assigned
                continue

            next_mask = mask | (1 << worker)
            dp[next_mask] = min(dp[next_mask],
                               dp[mask] + cost[worker][jobs_assigned])

    return dp[(1 << n) - 1]

# Example: 3 workers, 3 jobs
cost = [
    [9, 2, 7],  # Worker 0's cost for jobs 0, 1, 2
    [6, 4, 3],  # Worker 1's cost
    [5, 8, 1]   # Worker 2's cost
]
print(f"Minimum assignment cost: {min_cost_assignment(cost, 3)}")
# Optimal: Worker 0→Job 1 (2), Worker 1→Job 2 (3), Worker 2→Job 0 (5) = 10
```

### Pattern 3: Partition DP

**Problem**: Merge/partition items optimally (like the merge lists problem).

**State**: `dp[mask]` = minimum cost to merge all items in `mask`

```python
def optimal_partition_dp(items, n):
    """
    Generic partition DP template.
    Find optimal way to partition/merge items.

    State: dp[mask] = (min_cost, merged_result)
    Transition: Try all ways to split mask into two parts

    Time: O(3^n) - for each mask, enumerate all submasks
    Space: O(2^n)
    """
    # dp[mask] = (cost, data)
    dp = {}

    # Base cases: single items
    for i in range(n):
        dp[1 << i] = (0, items[i])

    # Process all masks in increasing order of popcount
    for mask in range(1, 1 << n):
        if mask in dp:  # Base case
            continue

        min_cost = float('inf')
        best_result = None

        # Try all ways to partition mask
        submask = mask
        while submask > 0:
            complement = mask ^ submask

            # Both parts must be non-empty and computed
            if complement > 0 and submask in dp and complement in dp:
                cost1, data1 = dp[submask]
                cost2, data2 = dp[complement]

                # Cost to merge these two parts
                merge_cost = compute_merge_cost(data1, data2)
                total_cost = cost1 + cost2 + merge_cost

                if total_cost < min_cost:
                    min_cost = total_cost
                    best_result = merge_data(data1, data2)

            submask = (submask - 1) & mask

        if best_result is not None:
            dp[mask] = (min_cost, best_result)

    full_mask = (1 << n) - 1
    return dp[full_mask][0]

# Helper functions (problem-specific)
def compute_merge_cost(data1, data2):
    # Example: cost based on sizes and medians
    return len(data1) + len(data2) + abs(median(data1) - median(data2))

def merge_data(data1, data2):
    # Merge sorted lists, concatenate, etc.
    return sorted(data1 + data2)
```

### Pattern 4: Maximum Independent Set

**Problem**: Select maximum subset with no two adjacent elements.

```python
def max_independent_set(adj, n):
    """
    Find maximum independent set in a graph.

    State: dp[mask] = max independent set size for nodes in mask
    Constraint: No two selected nodes can be adjacent

    Time: O(2^n * n^2)
    Space: O(2^n)
    """
    dp = [0] * (1 << n)

    # Check all subsets
    for mask in range(1 << n):
        # Check if mask is an independent set
        is_independent = True
        for i in range(n):
            if not (mask & (1 << i)):
                continue
            for j in range(i + 1, n):
                if not (mask & (1 << j)):
                    continue
                if adj[i][j]:  # i and j are adjacent
                    is_independent = False
                    break
            if not is_independent:
                break

        if is_independent:
            dp[mask] = bin(mask).count('1')
        else:
            # Try removing one node
            for i in range(n):
                if mask & (1 << i):
                    dp[mask] = max(dp[mask], dp[mask ^ (1 << i)])

    return dp[(1 << n) - 1]

# Example: Graph with 4 nodes
adj = [
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [0, 1, 1, 0]
]
print(f"Max independent set size: {max_independent_set(adj, 4)}")
# Optimal: nodes {0, 3} or {1, 2}, size = 2
```

---

## 4. Advanced Bit Tricks

### Isolation and Manipulation

```python
# ============================================
# ISOLATE AND MANIPULATE SPECIFIC BITS
# ============================================

# Isolate rightmost 1-bit
def rightmost_1(x):
    return x & -x
    # 10110 → 00010

# Isolate rightmost 0-bit (turn it to 1)
def rightmost_0(x):
    return ~x & (x + 1)
    # 10101 → 00010

# Turn off rightmost 1-bit
def turn_off_rightmost_1(x):
    return x & (x - 1)
    # 10110 → 10100

# Turn on rightmost 0-bit
def turn_on_rightmost_0(x):
    return x | (x + 1)
    # 10101 → 10111

# Isolate rightmost block of 1s
def rightmost_block(x):
    return x ^ (x - 1)
    # 10111000 → 00000111 (last block of 1s)

# Turn off rightmost block of 1s
def turn_off_block(x):
    return x & (x + 1)
    # 10111000 → 10000000
```

### Swap and Reverse

```python
# ============================================
# SWAP AND REVERSE BITS
# ============================================

def swap_bits(x, i, j):
    """Swap bits at positions i and j"""
    if ((x >> i) & 1) != ((x >> j) & 1):
        x ^= (1 << i) | (1 << j)
    return x

def reverse_bits(x, width=32):
    """Reverse bits of a number"""
    result = 0
    for _ in range(width):
        result = (result << 1) | (x & 1)
        x >>= 1
    return result

# Example
x = 0b10110
print(f"Original: {x:05b}")
x = swap_bits(x, 1, 3)
print(f"After swapping bits 1 and 3: {x:05b}")

x = 0b10110
print(f"Reversed (5 bits): {reverse_bits(x, 5):05b}")
```

### Gray Code

```python
# ============================================
# GRAY CODE GENERATION
# ============================================

def gray_code(n):
    """
    Generate all 2^n Gray codes.
    Gray code: Adjacent codes differ by exactly 1 bit.

    Formula: gray(i) = i XOR (i >> 1)
    """
    return [i ^ (i >> 1) for i in range(1 << n)]

def inverse_gray(gray):
    """Convert Gray code back to binary"""
    binary = gray
    gray >>= 1
    while gray:
        binary ^= gray
        gray >>= 1
    return binary

# Example: 3-bit Gray codes
codes = gray_code(3)
print("Gray codes:")
for i, code in enumerate(codes):
    print(f"{i:03b} → {code:03b} (Gray)")

# Verify adjacent codes differ by 1 bit
for i in range(len(codes) - 1):
    diff = codes[i] ^ codes[i + 1]
    assert bin(diff).count('1') == 1, "Not a valid Gray code!"
```

---

## 5. SOS (Sum Over Subsets) DP

### Standard SOS DP

**Problem**: For each mask, compute sum of values over all its submasks.

**Naive**: O(3^n) - for each mask, enumerate all submasks
**SOS DP**: O(n × 2^n) - much faster!

```python
def sos_dp(arr, n):
    """
    Sum Over Subsets DP.

    For each mask, compute: dp[mask] = Σ arr[submask] for all submasks of mask

    Key idea: Build up by considering one bit at a time.
    For bit i, dp[mask] = dp[mask with bit i off] + (dp[mask] if bit i is set)

    Time: O(n * 2^n)
    Space: O(2^n)
    """
    # Initialize with original array
    dp = arr[:]

    # For each bit position
    for i in range(n):
        # For each mask
        for mask in range(1 << n):
            # If bit i is set in mask
            if mask & (1 << i):
                # Add contribution from mask with bit i turned off
                dp[mask] += dp[mask ^ (1 << i)]

    return dp

# Example: Count number of submasks for each mask
n = 4
count = [1] * (1 << n)  # Each mask has itself as a submask
result = sos_dp(count, n)

print("Number of submasks (including self):")
for mask in range(1 << n):
    print(f"{mask:04b} ({mask:2d}) has {result[mask]:2d} submasks")

# Verification
for mask in range(1 << n):
    expected = 1 << bin(mask).count('1')  # 2^k where k = popcount
    assert result[mask] == expected
```

### Inverse SOS (Sum Over Supersets)

```python
def superset_dp(arr, n):
    """
    For each mask, compute sum over all supersets.

    Time: O(n * 2^n)
    """
    dp = arr[:]

    for i in range(n):
        for mask in range(1 << n):
            # If bit i is NOT set
            if not (mask & (1 << i)):
                # Add contribution from mask with bit i turned on
                dp[mask] += dp[mask | (1 << i)]

    return dp

# Example
n = 3
arr = [i for i in range(1 << n)]
result = superset_dp(arr, n)

print("Sum over supersets:")
for mask in range(1 << n):
    print(f"{mask:03b}: sum = {result[mask]}")
```

### Applications of SOS DP

```python
# ============================================
# APPLICATION 1: COUNT SUBSETS WITH PROPERTY
# ============================================

def count_subsets_with_and_zero(arr, n):
    """
    Count pairs (i, j) where arr[i] & arr[j] == 0.

    Approach: For each arr[i], count how many arr[j] are subsets of ~arr[i]
    """
    max_val = max(arr)
    bits = max_val.bit_length()

    # Count frequency of each value
    freq = [0] * (1 << bits)
    for x in arr:
        freq[x] += 1

    # SOS DP to get count of all submasks
    sos = sos_dp(freq, bits)

    # For each element, count compatible elements
    count = 0
    for x in arr:
        complement = ((1 << bits) - 1) ^ x  # All bits flipped
        count += sos[complement]
        if x == 0:  # Don't count self-pair
            count -= 1

    return count // 2  # Each pair counted twice


# ============================================
# APPLICATION 2: MAXIMUM XOR SUBSET
# ============================================

def max_xor_subset(nums):
    """
    Find subset with maximum XOR value.
    Uses Gaussian elimination on bit vectors.

    Time: O(n * log(MAX))
    """
    basis = []

    for num in nums:
        cur = num
        # Try to reduce cur using existing basis vectors
        for b in basis:
            cur = min(cur, cur ^ b)

        if cur != 0:
            basis.append(cur)
            basis.sort(reverse=True)

    # Maximum XOR is XOR of all basis vectors
    result = 0
    for b in basis:
        result ^= b

    return result
```

---

## 6. Common Problem Templates

### Template 1: Subset Selection DP

```python
def subset_selection_template(items, n):
    """
    Choose optimal subset of items.

    State: dp[mask] = optimal value for subset represented by mask
    """
    dp = [0] * (1 << n)

    # Base case
    dp[0] = 0  # Empty subset

    # Fill DP table
    for mask in range(1 << n):
        # Option 1: Try adding each item not in mask
        for i in range(n):
            if mask & (1 << i):
                continue

            next_mask = mask | (1 << i)
            dp[next_mask] = max(dp[next_mask],
                               dp[mask] + items[i])

        # Option 2: Transition from submasks
        # dp[mask] = max over all submasks

    return dp[(1 << n) - 1]
```

### Template 2: Position-Based DP

```python
def position_based_template(items, n):
    """
    Track both subset AND current position.

    State: dp[mask][pos] = optimal value for subset mask, currently at pos
    Common in TSP, Hamiltonian path problems.
    """
    INF = float('inf')
    dp = [[INF] * n for _ in range(1 << n)]

    # Base case: start at each position
    for i in range(n):
        dp[1 << i][i] = items[i]

    # Fill DP table
    for mask in range(1 << n):
        for last in range(n):
            if not (mask & (1 << last)):
                continue
            if dp[mask][last] == INF:
                continue

            # Try going to next position
            for next_pos in range(n):
                if mask & (1 << next_pos):
                    continue

                next_mask = mask | (1 << next_pos)
                transition_cost = cost(last, next_pos)
                dp[next_mask][next_pos] = min(
                    dp[next_mask][next_pos],
                    dp[mask][last] + transition_cost
                )

    # Return best ending position
    full_mask = (1 << n) - 1
    return min(dp[full_mask])
```

### Template 3: Profile DP (Grid Problems)

```python
def profile_dp_template(n, m):
    """
    Use bitmask to represent state of one dimension (column/row).
    Common in tiling problems.

    State: dp[col][profile] = ways to tile up to column col
           profile = bitmask representing which cells extend to next column

    Time: O(n * m * 2^m)
    """
    dp = [{} for _ in range(m + 1)]
    dp[0][0] = 1  # Base: empty grid

    for col in range(m):
        for profile, ways in dp[col].items():
            # Generate next profiles by filling current column
            fill_column(n, col, profile, 0, 0, ways, dp[col + 1])

    # Final state: no cells extending beyond last column
    return dp[m].get(0, 0)

def fill_column(rows, col, cur_profile, row, next_profile, ways, next_dp):
    """Recursively fill one column, generating next profile."""
    if row == rows:
        # Finished filling this column
        next_dp[next_profile] = next_dp.get(next_profile, 0) + ways
        return

    if cur_profile & (1 << row):
        # Cell already filled from previous column
        fill_column(rows, col, cur_profile, row + 1,
                   next_profile, ways, next_dp)
    else:
        # Option 1: Place vertical tile (occupies this and next row)
        if row + 1 < rows and not (cur_profile & (1 << (row + 1))):
            fill_column(rows, col, cur_profile | (1 << (row + 1)),
                       row + 2, next_profile, ways, next_dp)

        # Option 2: Place horizontal tile (extends to next column)
        fill_column(rows, col, cur_profile, row + 1,
                   next_profile | (1 << row), ways, next_dp)
```

---

## 7. Practice Problems

### Beginner Level

| Problem | Pattern | Key Technique |
|---------|---------|---------------|
| **Subset Sum** | Basic DP | Bitmask as DP state |
| **Hamming Distance** | Bit counting | Process bit-by-bit |
| **Single Number** | XOR properties | a ^ a = 0 |
| **Power of Two** | Bit check | n & (n-1) == 0 |

### Intermediate Level

| Problem | Pattern | Key Technique |
|---------|---------|---------------|
| **Assignment Problem** | Bitmask DP | dp[mask] with popcount |
| **Subset XOR** | XOR basis | Gaussian elimination |
| **Minimum Cost to Connect** | TSP variant | dp[mask][pos] |
| **Maximum Independent Set** | Graph + bitmask | Check adjacency |

### Advanced Level

| Problem | Pattern | Key Technique |
|---------|---------|---------------|
| **TSP** | Position DP | dp[mask][city] |
| **SOS DP Problems** | Subset sums | O(n * 2^n) optimization |
| **Partition DP** | Merge lists | Enumerate submask pairs |
| **Tiling Problems** | Profile DP | Column-by-column state |

---

## Complexity Quick Reference

| Technique | Time Complexity | Use Case |
|-----------|-----------------|----------|
| Iterate all subsets | O(2^n) | Basic enumeration |
| Iterate all submasks | O(3^n) total | Partition problems |
| SOS DP | O(n × 2^n) | Sum over subsets |
| Gosper's hack | O(C(n,k)) | k-element subsets |
| TSP DP | O(2^n × n²) | Shortest Hamiltonian path |
| Assignment DP | O(2^n × n) | Matching problems |
| Profile DP | O(n × m × 2^m) | Grid tiling |

**Practical Limits**:
- n ≤ 20: Safe for most bitmask DP (2^20 ≈ 1M)
- n ≤ 22: Feasible with optimization (2^22 ≈ 4M)
- n ≤ 24: Cutting edge (2^24 ≈ 16M, need good constants)
- n > 24: Consider meet-in-the-middle or other techniques

---

## Key Takeaways

1. **Bitmask = Subset**: n-bit integer represents subset of n elements
2. **Submask enumeration** is O(3^n) total: `submask = (submask - 1) & mask`
3. **SOS DP** reduces O(3^n) to O(n × 2^n) for subset aggregation
4. **Common patterns**:
   - Selection: dp[mask]
   - Ordering: dp[mask][pos]
   - Partitioning: enumerate submask pairs
5. **Bit tricks** provide O(1) set operations
6. **Practical limit**: n ≤ 20-24 elements

**When to use**:
- Small n (≤ 20-24)
- Need to track "which elements used"
- Subset/combination problems
- Optimization over all possible states

**When NOT to use**:
- Large n (> 25)
- Continuous/infinite state space
- Problems better solved with greedy/graph algorithms

---

## Additional Resources

- **CSES**: Hamiltonian Flights, Elevator Rides
- **Codeforces**: Bitmask DP tutorial by -is-this-fft-
- **CP Handbook**: Chapter on Bitmask DP
- **AtCoder DP Contest**: Problems M, O, X use bitmasks

---

*Happy Coding! Master these techniques and unlock efficient solutions to subset problems.* 🚀
