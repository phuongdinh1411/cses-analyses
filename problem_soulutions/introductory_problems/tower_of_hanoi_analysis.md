---
layout: simple
title: "Tower of Hanoi"
permalink: /problem_soulutions/introductory_problems/tower_of_hanoi_analysis
---

# Tower of Hanoi

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand recursive algorithms and the Tower of Hanoi problem
- Apply recursive thinking to solve the Tower of Hanoi puzzle
- Implement efficient recursive algorithms with proper move sequence generation
- Optimize recursive solutions using mathematical analysis and move optimization
- Handle edge cases in recursive problems (base cases, large n, move sequence validation)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Recursive algorithms, Tower of Hanoi, recursive thinking, move sequence generation
- **Data Structures**: Recursive call stacks, move tracking, sequence generation, recursive data structures
- **Mathematical Concepts**: Recursive mathematics, Tower of Hanoi theory, move sequence mathematics, recursive analysis
- **Programming Skills**: Recursive implementation, move sequence generation, recursive thinking, algorithm implementation
- **Related Problems**: Recursive problems, Tower of Hanoi variants, Recursive thinking, Move sequence problems

## Problem Description

**Problem**: Move n disks from the first tower to the third tower using the second tower as auxiliary, following these rules:
1. Only one disk can be moved at a time
2. A larger disk cannot be placed on top of a smaller disk
3. Only the top disk of any tower can be moved

**Input**: An integer n (1 ≤ n ≤ 16)

**Output**: Print the moves required to solve the puzzle.

**Constraints**:
- 1 ≤ n ≤ 16
- Only one disk can be moved at a time
- Larger disk cannot be placed on top of smaller disk
- Only the top disk of any tower can be moved
- Must move all disks from tower 1 to tower 3
- Use tower 2 as auxiliary

**Example**:
```
Input: 3

Output:
1 3
1 2
3 2
1 3
2 1
2 3
1 3

Explanation: This shows the sequence of moves to solve the puzzle with 3 disks.
```

## Visual Example

### Input and Problem Setup
```
Input: n = 3 (3 disks)

Initial Setup:
Tower 1: [3, 2, 1]  (largest at bottom, smallest at top)
Tower 2: []         (empty auxiliary tower)
Tower 3: []         (empty destination tower)

Goal: Move all disks from Tower 1 to Tower 3
```

### Move Sequence Visualization
```
Step 1: Move disk 1 from Tower 1 to Tower 3
Tower 1: [3, 2]
Tower 2: []
Tower 3: [1]

Step 2: Move disk 2 from Tower 1 to Tower 2
Tower 1: [3]
Tower 2: [2]
Tower 3: [1]

Step 3: Move disk 1 from Tower 3 to Tower 2
Tower 1: [3]
Tower 2: [2, 1]
Tower 3: []

Step 4: Move disk 3 from Tower 1 to Tower 3
Tower 1: []
Tower 2: [2, 1]
Tower 3: [3]

Step 5: Move disk 1 from Tower 2 to Tower 1
Tower 1: [1]
Tower 2: [2]
Tower 3: [3]

Step 6: Move disk 2 from Tower 2 to Tower 3
Tower 1: [1]
Tower 2: []
Tower 3: [3, 2]

Step 7: Move disk 1 from Tower 1 to Tower 3
Tower 1: []
Tower 2: []
Tower 3: [3, 2, 1]
```

### Recursive Pattern Analysis
```
For n = 3:
1. Move 2 disks from Tower 1 to Tower 2 (using Tower 3 as auxiliary)
2. Move largest disk from Tower 1 to Tower 3
3. Move 2 disks from Tower 2 to Tower 3 (using Tower 1 as auxiliary)

This follows the recursive pattern:
- Solve for n-1 disks
- Move largest disk
- Solve for n-1 disks again
```

### Mathematical Properties
```
Total moves required: 2^n - 1
For n = 3: 2^3 - 1 = 8 - 1 = 7 moves

Each disk moves exactly 2^(n-i) times:
- Disk 1 (smallest): 2^(3-1) = 4 times
- Disk 2 (medium): 2^(3-2) = 2 times  
- Disk 3 (largest): 2^(3-3) = 1 time
```

### Key Insight
The solution works by:
1. Using recursive approach to break down the problem
2. Moving n-1 disks to auxiliary tower
3. Moving largest disk to destination
4. Moving n-1 disks from auxiliary to destination
5. Time complexity: O(2^n) for generating all moves
6. Space complexity: O(n) for recursion depth

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Naive Iterative Simulation (Inefficient)

**Key Insights from Naive Solution:**
- Simulate the puzzle step by step
- Use iterative approach to find valid moves
- Simple but computationally expensive approach
- Not suitable for large inputs due to exponential growth

**Algorithm:**
1. Represent the three towers as stacks
2. Try all possible moves at each step
3. Use backtracking to find valid sequences
4. Generate the complete move sequence

**Visual Example:**
```
Naive approach: Try all possible moves
For n = 2:

Initial state:
Tower 1: [2, 1]
Tower 2: []
Tower 3: []

Possible moves from Tower 1:
- Move disk 1 to Tower 2: [2] [] [1]
- Move disk 1 to Tower 3: [2] [] [1]

Try first option:
Tower 1: [2]
Tower 2: []
Tower 3: [1]

Possible moves:
- Move disk 2 to Tower 2: [] [2] [1]
- Move disk 2 to Tower 3: [] [] [2,1] ❌ (invalid - larger on smaller)

This leads to exponential time complexity
```

**Implementation:**
```python
def tower_of_hanoi_naive(n):
    towers = [[i for i in range(n, 0, -1)], [], []]
    moves = []
    
    def is_valid_move(from_tower, to_tower):
        if not towers[from_tower]:
            return False
        if not towers[to_tower]:
            return True
        return towers[from_tower][-1] < towers[to_tower][-1]
    
    def make_move(from_tower, to_tower):
        disk = towers[from_tower].pop()
        towers[to_tower].append(disk)
        moves.append(f"{from_tower + 1} {to_tower + 1}")
    
    def solve_recursive():
        if len(towers[2]) == n:
            return True
        
        for from_tower in range(3):
            for to_tower in range(3):
                if from_tower != to_tower and is_valid_move(from_tower, to_tower):
                    make_move(from_tower, to_tower)
                    if solve_recursive():
                        return True
                    # Backtrack
                    disk = towers[to_tower].pop()
                    towers[from_tower].append(disk)
                    moves.pop()
        
        return False
    
    solve_recursive()
    return moves

def solve_tower_of_hanoi_naive():
    n = int(input())
    moves = tower_of_hanoi_naive(n)
    
    print(len(moves))
    for move in moves:
        print(move)
```

**Time Complexity:** O(3^n) for trying all possible move sequences
**Space Complexity:** O(n) for tower representation

**Why it's inefficient:**
- O(3^n) time complexity grows exponentially
- Not suitable for competitive programming with large inputs
- Memory-intensive for large n
- Poor performance with exponential growth

### Approach 2: Recursive Solution (Better)

**Key Insights from Recursive Solution:**
- Use recursive approach to break down the problem
- More efficient than naive simulation
- Can handle larger inputs than naive approach
- Uses divide-and-conquer principles

**Algorithm:**
1. Base case: move 1 disk directly
2. Recursive case: solve for n-1 disks, then move largest disk
3. Use auxiliary tower for intermediate storage
4. Follow the optimal recursive strategy

**Visual Example:**
```
Recursive approach: Break down the problem
For n = 3:

Step 1: Move 2 disks from Tower 1 to Tower 2
- This is a subproblem of size 2
- Use Tower 3 as auxiliary

Step 2: Move largest disk from Tower 1 to Tower 3
- Direct move of disk 3

Step 3: Move 2 disks from Tower 2 to Tower 3
- This is another subproblem of size 2
- Use Tower 1 as auxiliary
```

**Implementation:**
```python
def tower_of_hanoi_recursive(n, from_rod, aux_rod, to_rod):
    if n == 1:
        print(f"{from_rod} {to_rod}")
        return
    
    # Move n-1 disks from source to auxiliary
    tower_of_hanoi_recursive(n - 1, from_rod, to_rod, aux_rod)
    
    # Move the largest disk from source to destination
    print(f"{from_rod} {to_rod}")
    
    # Move n-1 disks from auxiliary to destination
    tower_of_hanoi_recursive(n - 1, aux_rod, from_rod, to_rod)

def solve_tower_of_hanoi_recursive():
    n = int(input())
    
    # Print total number of moves
    total_moves = (1 << n) - 1
    print(total_moves)
    
    # Solve the puzzle
    tower_of_hanoi_recursive(n, 1, 2, 3)
```

**Time Complexity:** O(2^n) for generating all moves
**Space Complexity:** O(n) for recursion depth

**Why it's better:**
- O(2^n) time complexity is better than O(3^n)
- Uses recursive thinking for efficient solution
- Suitable for competitive programming
- Efficient for moderate inputs

### Approach 3: Optimized Recursive with Mathematical Analysis (Optimal)

**Key Insights from Optimized Solution:**
- Use mathematical analysis to understand the solution
- Most efficient approach for Tower of Hanoi problems
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use mathematical formula for total moves: 2^n - 1
2. Apply recursive strategy for move generation
3. Leverage mathematical properties for optimal solution
4. Use bit manipulation for efficient calculations

**Visual Example:**
```
Optimized approach: Mathematical analysis
For n = 3:

Mathematical properties:
- Total moves: 2^3 - 1 = 7
- Each disk moves exactly 2^(n-i) times
- Disk 1: 2^(3-1) = 4 times
- Disk 2: 2^(3-2) = 2 times
- Disk 3: 2^(3-3) = 1 time

Recursive strategy:
- Break problem into smaller subproblems
- Use optimal move sequence
- Follow mathematical pattern
```

**Implementation:**
```python
def solve_tower_of_hanoi():
    n = int(input())
    
    # Print total number of moves using bit manipulation
    total_moves = (1 << n) - 1
    print(total_moves)
    
    # Solve the puzzle using recursive approach
    tower_of_hanoi_recursive(n, 1, 2, 3)

def tower_of_hanoi_recursive(n, from_rod, aux_rod, to_rod):
    if n == 1:
        print(f"{from_rod} {to_rod}")
        return
    
    # Move n-1 disks from source to auxiliary
    tower_of_hanoi_recursive(n - 1, from_rod, to_rod, aux_rod)
    
    # Move the largest disk from source to destination
    print(f"{from_rod} {to_rod}")
    
    # Move n-1 disks from auxiliary to destination
    tower_of_hanoi_recursive(n - 1, aux_rod, from_rod, to_rod)

# Main execution
if __name__ == "__main__":
    solve_tower_of_hanoi()
```

**Time Complexity:** O(2^n) for generating all moves
**Space Complexity:** O(n) for recursion depth

**Why it's optimal:**
- O(2^n) time complexity is optimal for this problem
- Uses mathematical analysis for efficient solution
- Most efficient approach for competitive programming
- Standard method for Tower of Hanoi problems

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Tower of Hanoi with Different Rules
**Problem**: Tower of Hanoi where you can move multiple disks at once under certain conditions.

**Link**: [CSES Problem Set - Tower of Hanoi Extended](https://cses.fi/problemset/task/tower_of_hanoi_extended)

```python
def tower_of_hanoi_extended(n, max_move_size):
    def solve_extended(n, from_rod, aux_rod, to_rod):
        if n <= max_move_size:
            print(f"{from_rod} {to_rod} {n}")
            return
        
        # Move n-max_move_size disks to auxiliary
        solve_extended(n - max_move_size, from_rod, to_rod, aux_rod)
        
        # Move max_move_size disks to destination
        print(f"{from_rod} {to_rod} {max_move_size}")
        
        # Move n-max_move_size disks from auxiliary to destination
        solve_extended(n - max_move_size, aux_rod, from_rod, to_rod)
    
    solve_extended(n, 1, 2, 3)
```

### Variation 2: Tower of Hanoi with Minimum Moves
**Problem**: Tower of Hanoi where you need to find the minimum number of moves to reach a specific configuration.

**Link**: [CSES Problem Set - Tower of Hanoi Minimum Moves](https://cses.fi/problemset/task/tower_of_hanoi_minimum_moves)

```python
def tower_of_hanoi_minimum_moves(n, target_config):
    def count_moves_to_config(n, current_config, target_config):
        if n == 0:
            return 0
        
        if current_config[n-1] == target_config[n-1]:
            return count_moves_to_config(n-1, current_config, target_config)
        
        # Need to move disk n to target position
        return (1 << (n-1)) + count_moves_to_config(n-1, current_config, target_config)
    
    return count_moves_to_config(n, [1] * n, target_config)
```

### Variation 3: Tower of Hanoi with Cost
**Problem**: Tower of Hanoi where each move has a different cost.

**Link**: [CSES Problem Set - Tower of Hanoi with Cost](https://cses.fi/problemset/task/tower_of_hanoi_cost)

```python
def tower_of_hanoi_with_cost(n, move_costs):
    def solve_with_cost(n, from_rod, aux_rod, to_rod):
        if n == 1:
            cost = move_costs[from_rod-1][to_rod-1]
            print(f"{from_rod} {to_rod} {cost}")
            return cost
        
        # Move n-1 disks from source to auxiliary
        cost1 = solve_with_cost(n - 1, from_rod, to_rod, aux_rod)
        
        # Move the largest disk from source to destination
        cost2 = move_costs[from_rod-1][to_rod-1]
        print(f"{from_rod} {to_rod} {cost2}")
        
        # Move n-1 disks from auxiliary to destination
        cost3 = solve_with_cost(n - 1, aux_rod, from_rod, to_rod)
        
        return cost1 + cost2 + cost3
    
    return solve_with_cost(n, 1, 2, 3)
```

## Problem Variations

### **Variation 1: Tower of Hanoi with Dynamic Updates**
**Problem**: Handle dynamic disk updates (add/remove/update disks) while maintaining optimal Tower of Hanoi solution efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic disk management.

```python
from collections import defaultdict

class DynamicTowerOfHanoi:
    def __init__(self, n_disks=0):
        self.n_disks = n_disks
        self.towers = {'A': list(range(n_disks, 0, -1)), 'B': [], 'C': []}
        self.move_count = 0
        self._update_hanoi_info()
    
    def _update_hanoi_info(self):
        """Update Tower of Hanoi feasibility information."""
        self.total_disks = sum(len(tower) for tower in self.towers.values())
        self.min_moves = self._calculate_min_moves()
        self.solution_feasibility = self._calculate_solution_feasibility()
    
    def _calculate_min_moves(self):
        """Calculate minimum moves required."""
        return (2 ** self.n_disks) - 1 if self.n_disks > 0 else 0
    
    def _calculate_solution_feasibility(self):
        """Calculate solution feasibility."""
        if self.n_disks == 0:
            return 1.0
        
        # Check if all disks are on one tower
        non_empty_towers = sum(1 for tower in self.towers.values() if tower)
        return 1.0 if non_empty_towers <= 1 else 0.0
    
    def add_disk(self, size, tower='A'):
        """Add disk to specified tower."""
        if tower in self.towers:
            self.towers[tower].append(size)
            self.n_disks = max(self.n_disks, size)
            self._update_hanoi_info()
    
    def remove_disk(self, tower):
        """Remove top disk from specified tower."""
        if tower in self.towers and self.towers[tower]:
            disk = self.towers[tower].pop()
            self._update_hanoi_info()
            return disk
        return None
    
    def move_disk(self, from_tower, to_tower):
        """Move top disk from one tower to another."""
        if (from_tower in self.towers and to_tower in self.towers and 
            self.towers[from_tower] and 
            (not self.towers[to_tower] or self.towers[from_tower][-1] < self.towers[to_tower][-1])):
            
            disk = self.towers[from_tower].pop()
            self.towers[to_tower].append(disk)
            self.move_count += 1
            self._update_hanoi_info()
            return True
        return False
    
    def solve_hanoi(self, n=None, source='A', destination='C', auxiliary='B'):
        """Solve Tower of Hanoi recursively."""
        if n is None:
            n = self.n_disks
        
        if n == 0:
            return []
        
        moves = []
        
        # Move n-1 disks from source to auxiliary
        moves.extend(self.solve_hanoi(n-1, source, auxiliary, destination))
        
        # Move the largest disk from source to destination
        if self.move_disk(source, destination):
            moves.append(f"Move disk from {source} to {destination}")
        
        # Move n-1 disks from auxiliary to destination
        moves.extend(self.solve_hanoi(n-1, auxiliary, destination, source))
        
        return moves
    
    def get_solution_with_constraints(self, constraint_func):
        """Get solution that satisfies custom constraints."""
        if not self.towers['A']:
            return []
        
        if constraint_func(self.towers, self.move_count):
            return self.solve_hanoi()
        else:
            return []
    
    def get_solution_in_range(self, min_moves, max_moves):
        """Get solution within specified move range."""
        if min_moves <= self.min_moves <= max_moves:
            return self.solve_hanoi()
        else:
            return []
    
    def get_solution_with_pattern(self, pattern_func):
        """Get solution matching specified pattern."""
        if pattern_func(self.towers, self.move_count):
            return self.solve_hanoi()
        else:
            return []
    
    def get_tower_statistics(self):
        """Get statistics about the towers."""
        return {
            'total_disks': self.total_disks,
            'n_disks': self.n_disks,
            'min_moves': self.min_moves,
            'move_count': self.move_count,
            'solution_feasibility': self.solution_feasibility,
            'tower_distribution': {tower: len(disks) for tower, disks in self.towers.items()}
        }
    
    def get_hanoi_patterns(self):
        """Get patterns in Tower of Hanoi."""
        patterns = {
            'all_disks_on_source': 0,
            'all_disks_on_destination': 0,
            'disks_distributed': 0,
            'optimal_solution_possible': 0
        }
        
        # Check if all disks are on source tower
        if len(self.towers['A']) == self.n_disks and not self.towers['B'] and not self.towers['C']:
            patterns['all_disks_on_source'] = 1
        
        # Check if all disks are on destination tower
        if len(self.towers['C']) == self.n_disks and not self.towers['A'] and not self.towers['B']:
            patterns['all_disks_on_destination'] = 1
        
        # Check if disks are distributed across towers
        non_empty_towers = sum(1 for tower in self.towers.values() if tower)
        if non_empty_towers > 1:
            patterns['disks_distributed'] = 1
        
        # Check if optimal solution is possible
        if self.solution_feasibility == 1.0:
            patterns['optimal_solution_possible'] = 1
        
        return patterns
    
    def get_optimal_hanoi_strategy(self):
        """Get optimal strategy for Tower of Hanoi."""
        if self.n_disks == 0:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'solution_feasibility': 0
            }
        
        # Calculate efficiency rate
        efficiency_rate = self.solution_feasibility
        
        # Calculate solution feasibility
        solution_feasibility = self.solution_feasibility
        
        # Determine recommended strategy
        if self.n_disks <= 3:
            recommended_strategy = 'recursive_solution'
        elif self.n_disks <= 10:
            recommended_strategy = 'iterative_solution'
        else:
            recommended_strategy = 'optimized_solution'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'solution_feasibility': solution_feasibility
        }

# Example usage
n_disks = 3
dynamic_hanoi = DynamicTowerOfHanoi(n_disks)
print(f"Min moves: {dynamic_hanoi.min_moves}")
print(f"Solution feasibility: {dynamic_hanoi.solution_feasibility}")

# Add disk
dynamic_hanoi.add_disk(4, 'A')
print(f"After adding disk 4: {dynamic_hanoi.min_moves}")

# Remove disk
removed_disk = dynamic_hanoi.remove_disk('A')
print(f"After removing disk {removed_disk}: {dynamic_hanoi.min_moves}")

# Move disk
dynamic_hanoi.move_disk('A', 'B')
print(f"After moving disk: {dynamic_hanoi.move_count}")

# Get solution with constraints
def constraint_func(towers, move_count):
    return move_count <= 10

print(f"Solution with constraints: {len(dynamic_hanoi.get_solution_with_constraints(constraint_func))}")

# Get solution in range
print(f"Solution in range 5-15: {len(dynamic_hanoi.get_solution_in_range(5, 15))}")

# Get solution with pattern
def pattern_func(towers, move_count):
    return len(towers['A']) > 0

print(f"Solution with pattern: {len(dynamic_hanoi.get_solution_with_pattern(pattern_func))}")

# Get statistics
print(f"Statistics: {dynamic_hanoi.get_tower_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_hanoi.get_hanoi_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_hanoi.get_optimal_hanoi_strategy()}")
```

### **Variation 2: Tower of Hanoi with Different Operations**
**Problem**: Handle different types of Tower of Hanoi operations (weighted disks, priority-based moves, advanced tower analysis).

**Approach**: Use advanced data structures for efficient different types of Tower of Hanoi operations.

```python
class AdvancedTowerOfHanoi:
    def __init__(self, n_disks=0, weights=None, priorities=None):
        self.n_disks = n_disks
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.towers = {'A': list(range(n_disks, 0, -1)), 'B': [], 'C': []}
        self.move_count = 0
        self._update_hanoi_info()
    
    def _update_hanoi_info(self):
        """Update Tower of Hanoi feasibility information."""
        self.total_disks = sum(len(tower) for tower in self.towers.values())
        self.min_moves = self._calculate_min_moves()
        self.solution_feasibility = self._calculate_solution_feasibility()
    
    def _calculate_min_moves(self):
        """Calculate minimum moves required."""
        return (2 ** self.n_disks) - 1 if self.n_disks > 0 else 0
    
    def _calculate_solution_feasibility(self):
        """Calculate solution feasibility."""
        if self.n_disks == 0:
            return 1.0
        
        # Check if all disks are on one tower
        non_empty_towers = sum(1 for tower in self.towers.values() if tower)
        return 1.0 if non_empty_towers <= 1 else 0.0
    
    def get_weighted_solution(self):
        """Get solution with weights and priorities applied."""
        if not self.towers['A']:
            return []
        
        # Create weighted solution
        weighted_moves = []
        temp_towers = {tower: tower_disks[:] for tower, tower_disks in self.towers.items()}
        
        # Calculate weighted moves
        for tower, disks in temp_towers.items():
            for disk in disks:
                weight = self.weights.get(disk, 1)
                priority = self.priorities.get(disk, 1)
                weighted_score = weight * priority
                weighted_moves.append((disk, tower, weighted_score))
        
        # Sort by weighted score
        weighted_moves.sort(key=lambda x: x[2], reverse=True)
        
        return weighted_moves
    
    def get_solution_with_priority(self, priority_func):
        """Get solution considering priority."""
        if not self.towers['A']:
            return []
        
        # Create priority-based solution
        priority_moves = []
        for tower, disks in self.towers.items():
            for disk in disks:
                priority = priority_func(disk, tower, self.weights, self.priorities)
                priority_moves.append((disk, tower, priority))
        
        # Sort by priority
        priority_moves.sort(key=lambda x: x[2], reverse=True)
        return priority_moves
    
    def get_solution_with_optimization(self, optimization_func):
        """Get solution using custom optimization function."""
        if not self.towers['A']:
            return []
        
        # Create optimization-based solution
        optimized_moves = []
        for tower, disks in self.towers.items():
            for disk in disks:
                score = optimization_func(disk, tower, self.weights, self.priorities)
                optimized_moves.append((disk, tower, score))
        
        # Sort by optimization score
        optimized_moves.sort(key=lambda x: x[2], reverse=True)
        return optimized_moves
    
    def get_solution_with_constraints(self, constraint_func):
        """Get solution that satisfies custom constraints."""
        if not self.towers['A']:
            return []
        
        if constraint_func(self.towers, self.move_count, self.weights, self.priorities):
            return self.get_weighted_solution()
        else:
            return []
    
    def get_solution_with_multiple_criteria(self, criteria_list):
        """Get solution that satisfies multiple criteria."""
        if not self.towers['A']:
            return []
        
        satisfies_all_criteria = True
        for criterion in criteria_list:
            if not criterion(self.towers, self.move_count, self.weights, self.priorities):
                satisfies_all_criteria = False
                break
        
        if satisfies_all_criteria:
            return self.get_weighted_solution()
        else:
            return []
    
    def get_solution_with_alternatives(self, alternatives):
        """Get solution considering alternative weights/priorities."""
        result = []
        
        # Check original solution
        original_solution = self.get_weighted_solution()
        result.append((original_solution, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedTowerOfHanoi(self.n_disks, alt_weights, alt_priorities)
            temp_solution = temp_instance.get_weighted_solution()
            result.append((temp_solution, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_solution_with_adaptive_criteria(self, adaptive_func):
        """Get solution using adaptive criteria."""
        if not self.towers['A']:
            return []
        
        if adaptive_func(self.towers, self.move_count, self.weights, self.priorities, []):
            return self.get_weighted_solution()
        else:
            return []
    
    def get_hanoi_optimization(self):
        """Get optimal Tower of Hanoi configuration."""
        strategies = [
            ('weighted_solution', lambda: len(self.get_weighted_solution())),
            ('total_weight', lambda: sum(self.weights.values())),
            ('total_priority', lambda: sum(self.priorities.values())),
        ]
        
        best_strategy = None
        best_value = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                current_value = strategy_func()
                if current_value > best_value:
                    best_value = current_value
                    best_strategy = (strategy_name, current_value)
            except:
                continue
        
        return best_strategy

# Example usage
n_disks = 3
weights = {disk: disk * 2 for disk in range(1, n_disks + 1)}  # Weight based on disk size
priorities = {disk: n_disks - disk + 1 for disk in range(1, n_disks + 1)}  # Priority based on disk size
advanced_hanoi = AdvancedTowerOfHanoi(n_disks, weights, priorities)

print(f"Weighted solution: {len(advanced_hanoi.get_weighted_solution())}")

# Get solution with priority
def priority_func(disk, tower, weights, priorities):
    return weights.get(disk, 1) + priorities.get(disk, 1)

print(f"Solution with priority: {len(advanced_hanoi.get_solution_with_priority(priority_func))}")

# Get solution with optimization
def optimization_func(disk, tower, weights, priorities):
    return weights.get(disk, 1) * priorities.get(disk, 1)

print(f"Solution with optimization: {len(advanced_hanoi.get_solution_with_optimization(optimization_func))}")

# Get solution with constraints
def constraint_func(towers, move_count, weights, priorities):
    return move_count <= 10 and len(towers['A']) > 0

print(f"Solution with constraints: {len(advanced_hanoi.get_solution_with_constraints(constraint_func))}")

# Get solution with multiple criteria
def criterion1(towers, move_count, weights, priorities):
    return move_count <= 10

def criterion2(towers, move_count, weights, priorities):
    return len(towers['A']) > 0

criteria_list = [criterion1, criterion2]
print(f"Solution with multiple criteria: {len(advanced_hanoi.get_solution_with_multiple_criteria(criteria_list))}")

# Get solution with alternatives
alternatives = [({disk: 1 for disk in range(1, n_disks + 1)}, {disk: 1 for disk in range(1, n_disks + 1)}), ({disk: disk*3 for disk in range(1, n_disks + 1)}, {disk: disk+1 for disk in range(1, n_disks + 1)})]
print(f"Solution with alternatives: {len(advanced_hanoi.get_solution_with_alternatives(alternatives))}")

# Get solution with adaptive criteria
def adaptive_func(towers, move_count, weights, priorities, current_result):
    return move_count <= 10 and len(current_result) < 5

print(f"Solution with adaptive criteria: {len(advanced_hanoi.get_solution_with_adaptive_criteria(adaptive_func))}")

# Get hanoi optimization
print(f"Hanoi optimization: {advanced_hanoi.get_hanoi_optimization()}")
```

### **Variation 3: Tower of Hanoi with Constraints**
**Problem**: Handle Tower of Hanoi with additional constraints (move limits, disk constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedTowerOfHanoi:
    def __init__(self, n_disks=0, constraints=None):
        self.n_disks = n_disks
        self.constraints = constraints or {}
        self.towers = {'A': list(range(n_disks, 0, -1)), 'B': [], 'C': []}
        self.move_count = 0
        self._update_hanoi_info()
    
    def _update_hanoi_info(self):
        """Update Tower of Hanoi feasibility information."""
        self.total_disks = sum(len(tower) for tower in self.towers.values())
        self.min_moves = self._calculate_min_moves()
        self.solution_feasibility = self._calculate_solution_feasibility()
    
    def _calculate_min_moves(self):
        """Calculate minimum moves required."""
        return (2 ** self.n_disks) - 1 if self.n_disks > 0 else 0
    
    def _calculate_solution_feasibility(self):
        """Calculate solution feasibility."""
        if self.n_disks == 0:
            return 1.0
        
        # Check if all disks are on one tower
        non_empty_towers = sum(1 for tower in self.towers.values() if tower)
        return 1.0 if non_empty_towers <= 1 else 0.0
    
    def _is_valid_move(self, from_tower, to_tower):
        """Check if move is valid considering constraints."""
        # Basic move validation
        if (from_tower not in self.towers or to_tower not in self.towers or 
            not self.towers[from_tower] or 
            (self.towers[to_tower] and self.towers[from_tower][-1] >= self.towers[to_tower][-1])):
            return False
        
        # Move count constraints
        if 'max_moves' in self.constraints:
            if self.move_count >= self.constraints['max_moves']:
                return False
        
        # Disk constraints
        if 'forbidden_disks' in self.constraints:
            if self.towers[from_tower][-1] in self.constraints['forbidden_disks']:
                return False
        
        if 'required_disks' in self.constraints:
            if self.towers[from_tower][-1] not in self.constraints['required_disks']:
                return False
        
        # Pattern constraints
        if 'pattern_constraints' in self.constraints:
            for constraint in self.constraints['pattern_constraints']:
                if not constraint(self.towers, self.move_count):
                    return False
        
        return True
    
    def get_solution_with_move_constraints(self, max_moves):
        """Get solution considering move constraints."""
        if not self.towers['A']:
            return []
        
        if self.min_moves <= max_moves:
            return self.solve_hanoi()
        else:
            return []
    
    def get_solution_with_disk_constraints(self, disk_constraints):
        """Get solution considering disk constraints."""
        if not self.towers['A']:
            return []
        
        satisfies_constraints = True
        for constraint in disk_constraints:
            if not constraint(self.towers, self.move_count):
                satisfies_constraints = False
                break
        
        if satisfies_constraints:
            return self.solve_hanoi()
        else:
            return []
    
    def get_solution_with_pattern_constraints(self, pattern_constraints):
        """Get solution considering pattern constraints."""
        if not self.towers['A']:
            return []
        
        satisfies_pattern = True
        for constraint in pattern_constraints:
            if not constraint(self.towers, self.move_count):
                satisfies_pattern = False
                break
        
        if satisfies_pattern:
            return self.solve_hanoi()
        else:
            return []
    
    def get_solution_with_mathematical_constraints(self, constraint_func):
        """Get solution that satisfies custom mathematical constraints."""
        if not self.towers['A']:
            return []
        
        if constraint_func(self.towers, self.move_count):
            return self.solve_hanoi()
        else:
            return []
    
    def get_solution_with_optimization_constraints(self, optimization_func):
        """Get solution using custom optimization constraints."""
        if not self.towers['A']:
            return []
        
        # Calculate optimization score for solution
        score = optimization_func(self.towers, self.move_count)
        
        if score > 0:
            return self.solve_hanoi()
        else:
            return []
    
    def get_solution_with_multiple_constraints(self, constraints_list):
        """Get solution that satisfies multiple constraints."""
        if not self.towers['A']:
            return []
        
        satisfies_all_constraints = True
        for constraint in constraints_list:
            if not constraint(self.towers, self.move_count):
                satisfies_all_constraints = False
                break
        
        if satisfies_all_constraints:
            return self.solve_hanoi()
        else:
            return []
    
    def get_solution_with_priority_constraints(self, priority_func):
        """Get solution with priority-based constraints."""
        if not self.towers['A']:
            return []
        
        # Calculate priority for solution
        priority = priority_func(self.towers, self.move_count)
        
        if priority > 0:
            return self.solve_hanoi()
        else:
            return []
    
    def get_solution_with_adaptive_constraints(self, adaptive_func):
        """Get solution with adaptive constraints."""
        if not self.towers['A']:
            return []
        
        if adaptive_func(self.towers, self.move_count, []):
            return self.solve_hanoi()
        else:
            return []
    
    def solve_hanoi(self, n=None, source='A', destination='C', auxiliary='B'):
        """Solve Tower of Hanoi recursively."""
        if n is None:
            n = self.n_disks
        
        if n == 0:
            return []
        
        moves = []
        
        # Move n-1 disks from source to auxiliary
        moves.extend(self.solve_hanoi(n-1, source, auxiliary, destination))
        
        # Move the largest disk from source to destination
        if self._is_valid_move(source, destination):
            disk = self.towers[source].pop()
            self.towers[destination].append(disk)
            self.move_count += 1
            moves.append(f"Move disk {disk} from {source} to {destination}")
        
        # Move n-1 disks from auxiliary to destination
        moves.extend(self.solve_hanoi(n-1, auxiliary, destination, source))
        
        return moves
    
    def get_optimal_hanoi_strategy(self):
        """Get optimal Tower of Hanoi strategy considering all constraints."""
        strategies = [
            ('move_constraints', self.get_solution_with_move_constraints),
            ('disk_constraints', self.get_solution_with_disk_constraints),
            ('pattern_constraints', self.get_solution_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_score = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'move_constraints':
                    result = strategy_func(100)
                elif strategy_name == 'disk_constraints':
                    disk_constraints = [lambda t, mc: len(t['A']) > 0]
                    result = strategy_func(disk_constraints)
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda t, mc: mc <= 10]
                    result = strategy_func(pattern_constraints)
                
                if len(result) > best_score:
                    best_score = len(result)
                    best_strategy = (strategy_name, result)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'max_moves': 10,
    'forbidden_disks': [1, 2],
    'required_disks': [3],
    'pattern_constraints': [lambda t, mc: mc <= 10]
}

n_disks = 3
constrained_hanoi = ConstrainedTowerOfHanoi(n_disks, constraints)

print("Move-constrained solution:", len(constrained_hanoi.get_solution_with_move_constraints(10)))

print("Disk-constrained solution:", len(constrained_hanoi.get_solution_with_disk_constraints([lambda t, mc: len(t['A']) > 0])))

print("Pattern-constrained solution:", len(constrained_hanoi.get_solution_with_pattern_constraints([lambda t, mc: mc <= 10])))

# Mathematical constraints
def custom_constraint(towers, move_count):
    return move_count <= 10 and len(towers['A']) > 0

print("Mathematical constraint solution:", len(constrained_hanoi.get_solution_with_mathematical_constraints(custom_constraint)))

# Range constraints
def range_constraint(towers, move_count):
    return 5 <= move_count <= 15

range_constraints = [range_constraint]
print("Range-constrained solution:", len(constrained_hanoi.get_solution_with_move_constraints(15)))

# Multiple constraints
def constraint1(towers, move_count):
    return move_count <= 10

def constraint2(towers, move_count):
    return len(towers['A']) > 0

constraints_list = [constraint1, constraint2]
print("Multiple constraints solution:", len(constrained_hanoi.get_solution_with_multiple_constraints(constraints_list)))

# Priority constraints
def priority_func(towers, move_count):
    return move_count + len(towers['A'])

print("Priority-constrained solution:", len(constrained_hanoi.get_solution_with_priority_constraints(priority_func)))

# Adaptive constraints
def adaptive_func(towers, move_count, current_result):
    return move_count <= 10 and len(current_result) < 5

print("Adaptive constraint solution:", len(constrained_hanoi.get_solution_with_adaptive_constraints(adaptive_func)))

# Optimal strategy
optimal = constrained_hanoi.get_optimal_hanoi_strategy()
print(f"Optimal hanoi strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Tower of Hanoi](https://cses.fi/problemset/task/2165) - Basic Tower of Hanoi problem
- [Chessboard and Queens](https://cses.fi/problemset/task/1624) - Recursive backtracking problems
- [Creating Strings](https://cses.fi/problemset/task/1622) - Recursive string generation

#### **LeetCode Problems**
- [Tower of Hanoi](https://leetcode.com/problems/tower-of-hanoi/) - Classic Tower of Hanoi problem
- [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) - Recursive generation
- [Permutations](https://leetcode.com/problems/permutations/) - Recursive permutation generation
- [Subsets](https://leetcode.com/problems/subsets/) - Recursive subset generation

#### **Problem Categories**
- **Recursive Algorithms**: Divide-and-conquer, recursive thinking, recursive problem solving
- **Mathematical Sequences**: Move counting, pattern recognition, mathematical analysis
- **Divide and Conquer**: Problem decomposition, recursive structure, base case handling
- **Algorithm Design**: Recursive algorithms, mathematical algorithms, sequence generation

## 📚 Learning Points

1. **Recursive Thinking**: Essential for understanding divide-and-conquer algorithms
2. **Tower of Hanoi Theory**: Key technique for understanding recursive problems
3. **Mathematical Analysis**: Important for understanding move patterns
4. **Divide and Conquer**: Critical for understanding recursive problem solving
5. **Base Cases**: Foundation for recursive algorithm design
6. **Recursive Patterns**: Critical for understanding recursive problem structures

## 📝 Summary

The Tower of Hanoi problem demonstrates recursive algorithms and mathematical analysis concepts for efficient puzzle solving. We explored three approaches:

1. **Naive Iterative Simulation**: O(3^n) time complexity using backtracking simulation, inefficient due to exponential growth
2. **Recursive Solution**: O(2^n) time complexity using recursive approach, better approach for recursive problems
3. **Optimized Recursive with Mathematical Analysis**: O(2^n) time complexity with mathematical understanding, optimal approach for competitive programming

The key insights include understanding recursive thinking, using divide-and-conquer principles, and applying mathematical patterns for optimal performance. This problem serves as an excellent introduction to recursive algorithms and mathematical analysis in competitive programming.
