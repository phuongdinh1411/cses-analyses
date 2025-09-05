---
layout: simple
title: "Introductory Problems Summary"
permalink: /problem_soulutions/introductory_problems/summary
---

# Introductory Problems

Welcome to the Introductory Problems section! This category contains fundamental algorithmic problems that serve as an excellent starting point for learning competitive programming concepts.

## Key Concepts & Techniques

### Problem-Solving Techniques

#### Brute Force and Simulation
- **Brute Force**: Try all possible solutions
  - *When to use*: When problem size is small, when no obvious pattern
  - *Time*: Often exponential, but acceptable for small inputs
  - *Space*: Usually O(n) where n is input size
  - *Applications*: Small search spaces, pattern finding, verification
  - *Implementation*: Use loops, recursion, or backtracking
- **Simulation**: Follow problem rules step by step
  - *When to use*: When problem describes a process to simulate
  - *Time*: O(k) where k is number of steps
  - *Space*: O(n) where n is problem size
  - *Applications*: Game simulation, process simulation, algorithm simulation
  - *Implementation*: Use loops to simulate each step

#### Pattern Recognition
- **Mathematical Patterns**: Find mathematical relationships
  - *When to use*: When problem involves numbers or sequences
  - *Time*: O(1) after pattern is found
  - *Space*: O(1)
  - *Applications*: Number sequences, geometric patterns, arithmetic progressions
  - *Implementation*: Use mathematical formulas or closed-form solutions
- **Geometric Patterns**: Find spatial relationships
  - *When to use*: When problem involves grids or spatial arrangements
  - *Time*: O(1) after pattern is found
  - *Space*: O(1)
  - *Applications*: Grid problems, coordinate systems, spatial arrangements
  - *Implementation*: Use coordinate transformations or geometric formulas

#### Optimization Techniques
- **Greedy Algorithms**: Make locally optimal choices
  - *When to use*: When local optimality leads to global optimality
  - *Time*: Usually O(n log n) due to sorting
  - *Space*: O(1) additional space
  - *Applications*: Scheduling, selection, optimization problems
  - *Implementation*: Sort by some criteria, then make greedy choices
- **Dynamic Programming**: Solve subproblems optimally
  - *When to use*: When problem has overlapping subproblems
  - *Time*: O(n²) or O(n³) typically
  - *Space*: O(n) or O(n²)
  - *Applications*: Optimization problems, counting problems, path problems
  - *Implementation*: Use memoization or bottom-up DP

### Mathematical Concepts

#### Number Theory
- **Modular Arithmetic**: Operations with remainders
  - *When to use*: When dealing with large numbers or cyclic patterns
  - *Properties*: (a + b) mod m = ((a mod m) + (b mod m)) mod m
  - *Applications*: Large number calculations, cyclic problems, cryptography
  - *Implementation*: Use modulo operator, handle negative numbers carefully
- **Prime Numbers**: Numbers divisible only by 1 and themselves
  - *When to use*: When problem involves divisibility or factorization
  - *Properties*: Unique factorization, distribution, primality testing
  - *Applications*: Factorization, cryptography, number theory problems
  - *Implementation*: Use sieve of Eratosthenes, trial division, or probabilistic tests
- **GCD and LCM**: Greatest common divisor and least common multiple
  - *When to use*: When dealing with fractions, ratios, or divisibility
  - *Properties*: gcd(a,b) = gcd(b, a mod b), lcm(a,b) = (a*b)/gcd(a,b)
  - *Applications*: Fraction simplification, ratio problems, divisibility
  - *Implementation*: Use Euclidean algorithm for GCD

#### Combinatorics
- **Permutations**: Arrangements of objects
  - *When to use*: When order matters in arrangements
  - *Formula*: P(n,r) = n!/(n-r)!
  - *Applications*: Arrangement problems, ordering problems, sequence problems
  - *Implementation*: Use factorial calculation or recursive generation
- **Combinations**: Selections of objects
  - *When to use*: When order doesn't matter in selections
  - *Formula*: C(n,r) = n!/(r!(n-r)!)
  - *Applications*: Selection problems, counting problems, probability
  - *Implementation*: Use factorial calculation or Pascal's triangle
- **Catalan Numbers**: Special sequence for balanced parentheses
  - *When to use*: When dealing with balanced structures
  - *Formula*: Cₙ = (1/(n+1)) × C(2n,n)
  - *Applications*: Balanced parentheses, binary trees, polygon triangulation
  - *Implementation*: Use recurrence relation or closed formula

#### Game Theory
- **Nim Game**: Mathematical game theory
  - *When to use*: When dealing with impartial games
  - *Strategy*: XOR of all pile sizes, if 0 then losing position
  - *Applications*: Game analysis, strategy problems, competitive games
  - *Implementation*: Calculate XOR of all values
- **Grundy Numbers**: Game position analysis
  - *When to use*: When analyzing game positions
  - *Properties*: mex of reachable positions, XOR property
  - *Applications*: Game analysis, position evaluation, strategy
  - *Implementation*: Use recursive calculation with memoization

### Programming Skills

#### Array Manipulation
- **Array Traversal**: Process all elements
  - *When to use*: When you need to process all array elements
  - *Time*: O(n) where n is array size
  - *Space*: O(1) additional space
  - *Applications*: Searching, counting, transformation
  - *Implementation*: Use for loops, while loops, or iterators
- **Array Sorting**: Arrange elements in order
  - *When to use*: When you need elements in specific order
  - *Time*: O(n log n) for comparison sorts
  - *Space*: O(1) for in-place sorts
  - *Applications*: Ordering, searching, optimization
  - *Implementation*: Use built-in sort functions or implement sorting algorithms
- **Array Searching**: Find specific elements
  - *When to use*: When you need to find elements with specific properties
  - *Time*: O(n) for linear search, O(log n) for binary search
  - *Space*: O(1) additional space
  - *Applications*: Element finding, position determination, existence checking
  - *Implementation*: Use linear search or binary search

#### String Processing
- **String Manipulation**: Modify string content
  - *When to use*: When you need to change string content
  - *Time*: O(n) where n is string length
  - *Space*: O(n) for new strings
  - *Applications*: Text processing, string transformation, parsing
  - *Implementation*: Use string functions, character arrays, or string builders
- **String Matching**: Find patterns in strings
  - *When to use*: When you need to find specific patterns
  - *Time*: O(n) for simple patterns, O(n+m) for complex patterns
  - *Space*: O(m) where m is pattern length
  - *Applications*: Pattern recognition, text analysis, parsing
  - *Implementation*: Use string search functions or pattern matching algorithms
- **String Analysis**: Analyze string properties
  - *When to use*: When you need to understand string characteristics
  - *Time*: O(n) where n is string length
  - *Space*: O(k) where k is number of distinct characters
  - *Applications*: Character counting, frequency analysis, property checking
  - *Implementation*: Use hash maps, arrays, or character counting

#### Bit Manipulation
- **Bit Operations**: Manipulate individual bits
  - *When to use*: When you need to work with binary representations
  - *Time*: O(1) for most operations
  - *Space*: O(1) additional space
  - *Applications*: Set operations, bitwise logic, optimization
  - *Implementation*: Use bitwise operators (AND, OR, XOR, NOT, shifts)
- **Bit Counting**: Count set bits
  - *When to use*: When you need to count 1s in binary representation
  - *Time*: O(log n) where n is the number
  - *Space*: O(1) additional space
  - *Applications*: Set size, population count, bit analysis
  - *Implementation*: Use bit manipulation or built-in functions
- **Bit Sets**: Use bits to represent sets
  - *When to use*: When you need to represent small sets efficiently
  - *Time*: O(1) for most operations
  - *Space*: O(1) for small sets
  - *Applications*: Set operations, subset enumeration, state representation
  - *Implementation*: Use integers as bit sets, manipulate with bit operations

#### Recursion and Backtracking
- **Recursive Solutions**: Solve problems recursively
  - *When to use*: When problem has recursive structure
  - *Time*: Often exponential, but can be optimized
  - *Space*: O(depth) for recursion stack
  - *Applications*: Tree problems, divide and conquer, recursive algorithms
  - *Implementation*: Define base case and recursive case
- **Backtracking**: Explore all possible solutions
  - *When to use*: When you need to find all valid solutions
  - *Time*: Often exponential
  - *Space*: O(depth) for recursion stack
  - *Applications*: Constraint satisfaction, puzzle solving, enumeration
  - *Implementation*: Use recursion with state tracking and pruning
- **Memoization**: Cache recursive results
  - *When to use*: When recursive calls repeat
  - *Time*: Reduces from exponential to polynomial
  - *Space*: O(n) for cache
  - *Applications*: Dynamic programming, optimization, repeated calculations
  - *Implementation*: Use hash map or array to store results

### Specialized Techniques

#### Grid and Coordinate Systems
- **Grid Traversal**: Move through grid cells
  - *When to use*: When problem involves grid-based movement
  - *Time*: O(rows × cols)
  - *Space*: O(rows × cols) for visited tracking
  - *Applications*: Path finding, grid analysis, spatial problems
  - *Implementation*: Use BFS, DFS, or coordinate-based loops
- **Coordinate Transformation**: Change coordinate systems
  - *When to use*: When you need to work in different coordinate systems
  - *Time*: O(1) per transformation
  - *Space*: O(1) additional space
  - *Applications*: Geometric problems, coordinate mapping, transformations
  - *Implementation*: Use mathematical formulas for coordinate conversion

#### Optimization Strategies
- **Space-Time Tradeoffs**: Balance memory and computation
  - *When to use*: When you can trade memory for speed or vice versa
  - *Example*: Precompute values vs. compute on demand
  - *Applications*: Performance optimization, memory management
  - *Implementation*: Use caching, precomputation, or lazy evaluation
- **Algorithm Selection**: Choose appropriate algorithm
  - *When to use*: When multiple algorithms solve the problem
  - *Example*: Use sorting for small arrays, use hash maps for large arrays
  - *Applications*: Performance optimization, problem solving
  - *Implementation*: Analyze problem constraints and choose accordingly

## Problem Categories

### Basic Algorithms
- [Weird Algorithm](weird_algorithm_analysis) - Learn basic number sequence manipulation
- [Missing Number](missing_number_analysis) - Find a missing number in a sequence
- [Repetitions](repetitions_analysis) - Handle repeated characters in strings

### Array and String Manipulation
- [Increasing Array](increasing_array_analysis) - Make array non-decreasing
- [Number Spiral](number_spiral_analysis) - Generate number spiral pattern
- [Palindrome Reorder](palindrome_reorder_analysis) - Rearrange string to palindrome
- [String Reorder](string_reorder_analysis) - Reorder string characters

### Mathematical Problems
- [Two Knights](two_knights_analysis) - Count knight placements on chessboard
- [Two Sets](two_sets_analysis) - Divide numbers into two equal sum sets
- [Bit Strings](bit_strings_analysis) - Count binary strings
- [Trailing Zeros](trailing_zeros_analysis) - Count trailing zeros in factorial

### Combinatorics and Permutations
- [Permutations](permutations_analysis) - Generate all permutations
- [Creating Strings](creating_strings_analysis) - Count string arrangements
- [Gray Code](gray_code_analysis) - Generate Gray code sequence

### Grid and Pattern Problems
- [Chessboard and Queens](chessboard_and_queens_analysis) - Place queens on chessboard
- [Grid Coloring I](grid_coloring_i_analysis) - Color grid cells
- [Grid Path Description](grid_path_description_analysis) - Describe grid paths
- [Knight Moves Grid](knight_moves_grid_analysis) - Knight movement on grid

### Optimization Problems
- [Apple Division](apple_division_analysis) - Minimize difference between apple groups
- [Mex Grid Construction](mex_grid_construction_analysis) - Construct MEX grid
- [Mex Grid Construction II](mex_grid_construction_ii_analysis) - Advanced MEX grid

### Game Theory
- [Coin Piles](coin_piles_analysis) - Remove coins from two piles
- [Tower of Hanoi](tower_of_hanoi_analysis) - Solve Tower of Hanoi puzzle
- [Raab Game I](raab_game_i_analysis) - Strategy for Raab's game

### Advanced Problems
- [Digit Queries](digit_queries_analysis) - Find digits in concatenated numbers

## Detailed Examples and Implementations

### Classic Introductory Problem Patterns with Code

#### 1. Mathematical and Number Theory Problems
```python
def gcd(a, b):
    """Calculate Greatest Common Divisor using Euclidean algorithm"""
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """Calculate Least Common Multiple"""
    return abs(a * b) // gcd(a, b)

def extended_gcd(a, b):
    """Extended Euclidean algorithm - returns gcd, x, y such that ax + by = gcd(a,b)"""
    if a == 0:
        return b, 0, 1
    
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y

def mod_inverse(a, m):
    """Find modular inverse of a under modulo m"""
    gcd_val, x, y = extended_gcd(a, m)
    if gcd_val != 1:
        return None  # Inverse doesn't exist
    return (x % m + m) % m

def is_prime(n):
    """Check if number is prime"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def sieve_of_eratosthenes(n):
    """Generate all primes up to n using Sieve of Eratosthenes"""
    if n < 2:
        return []
    
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    
    return [i for i in range(2, n + 1) if is_prime[i]]

def prime_factors(n):
    """Find prime factors of a number"""
    factors = []
    d = 2
    
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    
    if n > 1:
        factors.append(n)
    
    return factors

def factorial(n, mod=None):
    """Calculate factorial of n"""
    result = 1
    for i in range(1, n + 1):
        result *= i
        if mod:
            result %= mod
    return result

def modular_power(base, exponent, mod):
    """Calculate (base^exponent) % mod efficiently"""
    result = 1
    base = base % mod
    
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % mod
        exponent = exponent >> 1
        base = (base * base) % mod
    
    return result

def catalan_number(n):
    """Calculate nth Catalan number"""
    if n <= 1:
        return 1
    
    catalan = [0] * (n + 1)
    catalan[0] = catalan[1] = 1
    
    for i in range(2, n + 1):
        for j in range(i):
            catalan[i] += catalan[j] * catalan[i - j - 1]
    
    return catalan[n]

def fibonacci(n, mod=None):
    """Calculate nth Fibonacci number efficiently"""
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
        if mod:
            b %= mod
    
    return b
```

#### 2. Array Manipulation and Processing
```python
def find_missing_number(arr, n):
    """Find missing number in array containing numbers 1 to n"""
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(arr)
    return expected_sum - actual_sum

def find_duplicate_number(arr):
    """Find duplicate number in array using Floyd's cycle detection"""
    # Phase 1: Find intersection point in cycle
    slow = fast = arr[0]
    while True:
        slow = arr[slow]
        fast = arr[arr[fast]]
        if slow == fast:
            break
    
    # Phase 2: Find entrance to cycle
    slow = arr[0]
    while slow != fast:
        slow = arr[slow]
        fast = arr[fast]
    
    return slow

def two_sum(arr, target):
    """Find two numbers that sum to target"""
    num_map = {}
    for i, num in enumerate(arr):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []

def three_sum(arr, target):
    """Find three numbers that sum to target"""
    arr.sort()
    n = len(arr)
    result = []
    
    for i in range(n - 2):
        if i > 0 and arr[i] == arr[i - 1]:
            continue
        
        left, right = i + 1, n - 1
        while left < right:
            current_sum = arr[i] + arr[left] + arr[right]
            if current_sum == target:
                result.append([arr[i], arr[left], arr[right]])
                while left < right and arr[left] == arr[left + 1]:
                    left += 1
                while left < right and arr[right] == arr[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif current_sum < target:
                left += 1
            else:
                right -= 1
    
    return result

def maximum_subarray_sum(arr):
    """Find maximum sum of contiguous subarray (Kadane's algorithm)"""
    max_ending_here = max_so_far = arr[0]
    
    for i in range(1, len(arr)):
        max_ending_here = max(arr[i], max_ending_here + arr[i])
        max_so_far = max(max_so_far, max_ending_here)
    
    return max_so_far

def rotate_array(arr, k):
    """Rotate array to the right by k steps"""
    n = len(arr)
    k = k % n
    
    def reverse(start, end):
        while start < end:
            arr[start], arr[end] = arr[end], arr[start]
            start += 1
            end -= 1
    
    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)

def find_peak_element(arr):
    """Find a peak element in array (greater than neighbors)"""
    left, right = 0, len(arr) - 1
    
    while left < right:
        mid = (left + right) // 2
        if arr[mid] > arr[mid + 1]:
            right = mid
        else:
            left = mid + 1
    
    return left

def product_except_self(arr):
    """Calculate product of all elements except self"""
    n = len(arr)
    result = [1] * n
    
    # Calculate left products
    for i in range(1, n):
        result[i] = result[i - 1] * arr[i - 1]
    
    # Calculate right products and multiply
    right_product = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right_product
        right_product *= arr[i]
    
    return result
```

#### 3. String Processing and Manipulation
```python
def is_palindrome(s):
    """Check if string is palindrome"""
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

def longest_common_prefix(strs):
    """Find longest common prefix among strings"""
    if not strs:
        return ""
    
    prefix = strs[0]
    for i in range(1, len(strs)):
        while not strs[i].startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    
    return prefix

def valid_parentheses(s):
    """Check if parentheses are valid"""
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            stack.append(char)
    
    return not stack

def group_anagrams(strs):
    """Group strings that are anagrams of each other"""
    from collections import defaultdict
    
    anagram_groups = defaultdict(list)
    
    for s in strs:
        # Sort characters to create key
        key = ''.join(sorted(s))
        anagram_groups[key].append(s)
    
    return list(anagram_groups.values())

def longest_substring_without_repeating(s):
    """Find length of longest substring without repeating characters"""
    char_set = set()
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        char_set.add(s[right])
        max_length = max(max_length, right - left + 1)
    
    return max_length

def string_compression(s):
    """Compress string using run-length encoding"""
    if not s:
        return ""
    
    compressed = []
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            compressed.append(s[i - 1])
            if count > 1:
                compressed.append(str(count))
            count = 1
    
    compressed.append(s[-1])
    if count > 1:
        compressed.append(str(count))
    
    return ''.join(compressed)

def reverse_words(s):
    """Reverse words in string"""
    words = s.split()
    return ' '.join(reversed(words))

def is_anagram(s, t):
    """Check if two strings are anagrams"""
    if len(s) != len(t):
        return False
    
    char_count = {}
    for char in s:
        char_count[char] = char_count.get(char, 0) + 1
    
    for char in t:
        if char not in char_count or char_count[char] == 0:
            return False
        char_count[char] -= 1
    
    return True
```

#### 4. Bit Manipulation Techniques
```python
def count_set_bits(n):
    """Count number of set bits in binary representation"""
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count

def count_set_bits_brian_kernighan(n):
    """Count set bits using Brian Kernighan's algorithm"""
    count = 0
    while n:
        n &= (n - 1)  # Remove rightmost set bit
        count += 1
    return count

def is_power_of_two(n):
    """Check if number is power of 2"""
    return n > 0 and (n & (n - 1)) == 0

def get_bit(n, i):
    """Get bit at position i"""
    return (n >> i) & 1

def set_bit(n, i):
    """Set bit at position i"""
    return n | (1 << i)

def clear_bit(n, i):
    """Clear bit at position i"""
    return n & ~(1 << i)

def toggle_bit(n, i):
    """Toggle bit at position i"""
    return n ^ (1 << i)

def find_single_number(arr):
    """Find single number when all others appear twice (using XOR)"""
    result = 0
    for num in arr:
        result ^= num
    return result

def find_two_single_numbers(arr):
    """Find two single numbers when all others appear twice"""
    xor_result = 0
    for num in arr:
        xor_result ^= num
    
    # Find rightmost set bit
    rightmost_bit = xor_result & -xor_result
    
    # Separate numbers based on this bit
    num1 = num2 = 0
    for num in arr:
        if num & rightmost_bit:
            num1 ^= num
        else:
            num2 ^= num
    
    return [num1, num2]

def subset_sum_bitmask(arr, target):
    """Check if any subset sums to target using bitmask"""
    n = len(arr)
    
    for mask in range(1 << n):
        current_sum = 0
        for i in range(n):
            if mask & (1 << i):
                current_sum += arr[i]
        if current_sum == target:
            return True
    
    return False

def generate_all_subsets(arr):
    """Generate all possible subsets using bitmask"""
    n = len(arr)
    subsets = []
    
    for mask in range(1 << n):
        subset = []
        for i in range(n):
            if mask & (1 << i):
                subset.append(arr[i])
        subsets.append(subset)
    
    return subsets
```

#### 5. Recursion and Backtracking
```python
def generate_permutations(arr):
    """Generate all permutations using backtracking"""
    result = []
    
    def backtrack(current_perm):
        if len(current_perm) == len(arr):
            result.append(current_perm[:])
            return
        
        for num in arr:
            if num not in current_perm:
                current_perm.append(num)
                backtrack(current_perm)
                current_perm.pop()
    
    backtrack([])
    return result

def generate_combinations(arr, k):
    """Generate all combinations of size k"""
    result = []
    
    def backtrack(start, current_comb):
        if len(current_comb) == k:
            result.append(current_comb[:])
            return
        
        for i in range(start, len(arr)):
            current_comb.append(arr[i])
            backtrack(i + 1, current_comb)
            current_comb.pop()
    
    backtrack(0, [])
    return result

def solve_n_queens(n):
    """Solve N-Queens problem using backtracking"""
    result = []
    board = [['.' for _ in range(n)] for _ in range(n)]
    
    def is_safe(row, col):
        # Check column
        for i in range(row):
            if board[i][col] == 'Q':
                return False
        
        # Check diagonal
        for i, j in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
            if board[i][j] == 'Q':
                return False
        
        # Check anti-diagonal
        for i, j in zip(range(row - 1, -1, -1), range(col + 1, n)):
            if board[i][j] == 'Q':
                return False
        
        return True
    
    def backtrack(row):
        if row == n:
            result.append([''.join(row) for row in board])
            return
        
        for col in range(n):
            if is_safe(row, col):
                board[row][col] = 'Q'
                backtrack(row + 1)
                board[row][col] = '.'
    
    backtrack(0)
    return result

def generate_parentheses(n):
    """Generate all valid parentheses combinations"""
    result = []
    
    def backtrack(current, open_count, close_count):
        if len(current) == 2 * n:
            result.append(current)
            return
        
        if open_count < n:
            backtrack(current + '(', open_count + 1, close_count)
        
        if close_count < open_count:
            backtrack(current + ')', open_count, close_count + 1)
    
    backtrack('', 0, 0)
    return result

def word_search(board, word):
    """Search for word in 2D board using backtracking"""
    if not board or not word:
        return False
    
    rows, cols = len(board), len(board[0])
    
    def dfs(row, col, index):
        if index == len(word):
            return True
        
        if (row < 0 or row >= rows or col < 0 or col >= cols or 
            board[row][col] != word[index]):
            return False
        
        # Mark as visited
        temp = board[row][col]
        board[row][col] = '#'
        
        # Explore all directions
        found = (dfs(row + 1, col, index + 1) or
                dfs(row - 1, col, index + 1) or
                dfs(row, col + 1, index + 1) or
                dfs(row, col - 1, index + 1))
        
        # Restore
        board[row][col] = temp
        return found
    
    for i in range(rows):
        for j in range(cols):
            if dfs(i, j, 0):
                return True
    
    return False
```

#### 6. Grid and Coordinate Problems
```python
def number_of_islands(grid):
    """Count number of islands in 2D grid"""
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    islands = 0
    
    def dfs(row, col):
        if (row < 0 or row >= rows or col < 0 or col >= cols or 
            grid[row][col] != '1'):
            return
        
        grid[row][col] = '0'  # Mark as visited
        
        # Explore all directions
        dfs(row + 1, col)
        dfs(row - 1, col)
        dfs(row, col + 1)
        dfs(row, col - 1)
    
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '1':
                islands += 1
                dfs(i, j)
    
    return islands

def unique_paths(m, n):
    """Count unique paths from top-left to bottom-right"""
    # Using dynamic programming
    dp = [[1] * n for _ in range(m)]
    
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    
    return dp[m - 1][n - 1]

def unique_paths_with_obstacles(grid):
    """Count unique paths with obstacles"""
    if not grid or grid[0][0] == 1:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = 1
    
    # Initialize first row
    for j in range(1, cols):
        dp[0][j] = 0 if grid[0][j] == 1 else dp[0][j - 1]
    
    # Initialize first column
    for i in range(1, rows):
        dp[i][0] = 0 if grid[i][0] == 1 else dp[i - 1][0]
    
    # Fill the rest
    for i in range(1, rows):
        for j in range(1, cols):
            if grid[i][j] == 1:
                dp[i][j] = 0
            else:
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    
    return dp[rows - 1][cols - 1]

def spiral_matrix(matrix):
    """Return elements of matrix in spiral order"""
    if not matrix or not matrix[0]:
        return []
    
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        # Traverse right
        for j in range(left, right + 1):
            result.append(matrix[top][j])
        top += 1
        
        # Traverse down
        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1
        
        # Traverse left
        if top <= bottom:
            for j in range(right, left - 1, -1):
                result.append(matrix[bottom][j])
            bottom -= 1
        
        # Traverse up
        if left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1
    
    return result

def rotate_matrix(matrix):
    """Rotate matrix 90 degrees clockwise in-place"""
    n = len(matrix)
    
    # Transpose matrix
    for i in range(n):
        for j in range(i, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    
    # Reverse each row
    for i in range(n):
        matrix[i].reverse()

def set_matrix_zeroes(matrix):
    """Set entire row and column to zero if element is zero"""
    if not matrix or not matrix[0]:
        return
    
    rows, cols = len(matrix), len(matrix[0])
    first_row_zero = any(matrix[0][j] == 0 for j in range(cols))
    first_col_zero = any(matrix[i][0] == 0 for i in range(rows))
    
    # Mark rows and columns to be zeroed
    for i in range(1, rows):
        for j in range(1, cols):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0
    
    # Set zeros
    for i in range(1, rows):
        for j in range(1, cols):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
    
    # Handle first row and column
    if first_row_zero:
        for j in range(cols):
            matrix[0][j] = 0
    
    if first_col_zero:
        for i in range(rows):
            matrix[i][0] = 0
```

#### 7. Greedy Algorithms and Optimization
```python
def activity_selection(start, end):
    """Select maximum number of non-overlapping activities"""
    activities = list(zip(start, end))
    activities.sort(key=lambda x: x[1])  # Sort by end time
    
    selected = [activities[0]]
    last_end_time = activities[0][1]
    
    for i in range(1, len(activities)):
        if activities[i][0] >= last_end_time:
            selected.append(activities[i])
            last_end_time = activities[i][1]
    
    return selected

def fractional_knapsack(weights, values, capacity):
    """Solve fractional knapsack problem"""
    items = list(zip(weights, values))
    items.sort(key=lambda x: x[1] / x[0], reverse=True)  # Sort by value/weight ratio
    
    total_value = 0
    remaining_capacity = capacity
    
    for weight, value in items:
        if remaining_capacity >= weight:
            total_value += value
            remaining_capacity -= weight
        else:
            fraction = remaining_capacity / weight
            total_value += fraction * value
            break
    
    return total_value

def minimum_platforms(arrival, departure):
    """Find minimum number of platforms needed"""
    arrival.sort()
    departure.sort()
    
    platforms_needed = 1
    result = 1
    i = 1
    j = 0
    
    while i < len(arrival) and j < len(departure):
        if arrival[i] <= departure[j]:
            platforms_needed += 1
            i += 1
        else:
            platforms_needed -= 1
            j += 1
        
        result = max(result, platforms_needed)
    
    return result

def job_scheduling(jobs):
    """Schedule jobs to maximize profit (each job has deadline and profit)"""
    jobs.sort(key=lambda x: x[2], reverse=True)  # Sort by profit
    
    max_deadline = max(job[1] for job in jobs)
    schedule = [-1] * (max_deadline + 1)
    total_profit = 0
    
    for job in jobs:
        job_id, deadline, profit = job
        
        # Find latest available slot
        for j in range(deadline, 0, -1):
            if schedule[j] == -1:
                schedule[j] = job_id
                total_profit += profit
                break
    
    return total_profit, [job_id for job_id in schedule if job_id != -1]

def huffman_coding(frequencies):
    """Generate Huffman codes for characters"""
    import heapq
    
    class Node:
        def __init__(self, char, freq, left=None, right=None):
            self.char = char
            self.freq = freq
            self.left = left
            self.right = right
        
        def __lt__(self, other):
            return self.freq < other.freq
    
    # Create priority queue
    heap = [Node(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)
    
    # Build Huffman tree
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        
        merged = Node(None, left.freq + right.freq, left, right)
        heapq.heappush(heap, merged)
    
    # Generate codes
    codes = {}
    
    def generate_codes(node, code=""):
        if node.char is not None:
            codes[node.char] = code if code else "0"
        else:
            generate_codes(node.left, code + "0")
            generate_codes(node.right, code + "1")
    
    if heap:
        generate_codes(heap[0])
    
    return codes
```

## Tips for Success

1. **Read Carefully**: Understand the problem statement completely
2. **Start Simple**: Begin with the most basic solution
3. **Test Thoroughly**: Use all provided test cases
4. **Optimize Later**: First make it work, then make it fast
5. **Master Fundamentals**: Build strong foundation in basic algorithms
6. **Practice Patterns**: Recognize common problem patterns
7. **Handle Edge Cases**: Consider boundary conditions and special cases