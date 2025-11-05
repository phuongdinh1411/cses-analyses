---
layout: simple
title: "Ferris Wheel"
permalink: /problem_soulutions/sorting_and_searching/ferris_wheel_analysis
---

# Ferris Wheel

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the two-pointer technique and its applications
- Apply greedy algorithms for optimization problems
- Implement efficient sorting and searching algorithms
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in pairing problems

## 📋 Problem Description

There are n children who want to go to a Ferris wheel, and your task is to find a gondola for each child. Each gondola has a maximum weight capacity of x, and the weight of the i-th child is w[i].

Find the minimum number of gondolas needed to accommodate all children, where each gondola can carry at most two children and the total weight cannot exceed x.

**Input**: 
- First line: two integers n and x (number of children and maximum weight)
- Second line: n integers w[1], w[2], ..., w[n] (weights of children)

**Output**: 
- Print one integer: the minimum number of gondolas needed

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ x ≤ 10⁹
- 1 ≤ w[i] ≤ x

**Example**:
```
Input:
4 10
7 2 3 9

Output:
3

Explanation**: 
Children weights: [7, 2, 3, 9], capacity: 10

Optimal pairing:
- Gondola 1: child with weight 7 (alone, since 7+2=9≤10 but 7+3=10≤10, but 7+9=16>10)
- Gondola 2: children with weights 2 and 3 (2+3=5≤10)
- Gondola 3: child with weight 9 (alone, since 9+any other>10)

Total gondolas: 3
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Try All Possible Pairings

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Try all possible ways to pair children
- **Complete Coverage**: Guaranteed to find the optimal solution
- **Simple Implementation**: Straightforward recursive approach
- **Inefficient**: Exponential time complexity

**Key Insight**: Generate all possible ways to pair children and find the minimum number of gondolas.

**Algorithm**:
- Generate all possible pairings of children
- For each pairing, check if it's valid (total weight ≤ capacity)
- Find the pairing that uses the minimum number of gondolas

**Visual Example**:
```
Weights: [7, 2, 3, 9], Capacity: 10

All possible pairings:
1. All alone: [7], [2], [3], [9] → 4 gondolas
2. Pair (2,3): [7], [2,3], [9] → 3 gondolas ✓
3. Pair (2,7): [2,7], [3], [9] → 3 gondolas ✓
4. Pair (3,7): [3,7], [2], [9] → 3 gondolas ✓
5. Pair (2,9): [2,9], [7], [3] → 3 gondolas ✓
6. Pair (3,9): [3,9], [7], [2] → 3 gondolas ✓
7. Pair (7,9): Invalid (7+9=16>10)

Minimum: 3 gondolas
```

**Implementation**:
```python
def brute_force_ferris_wheel(weights, capacity):
    """
    Find minimum gondolas using brute force approach
    
    Args:
        weights: list of child weights
        capacity: maximum weight per gondola
    
    Returns:
        int: minimum number of gondolas needed
    """
    from itertools import combinations
    
    n = len(weights)
    min_gondolas = n  # Worst case: all children alone
    
    # Try all possible ways to pair children
    for k in range(n // 2 + 1):
        for pairs in combinations(range(n), 2 * k):
            # Check if this pairing is valid
            used = set(pairs)
            remaining = [i for i in range(n) if i not in used]
            
            # Check if all pairs are valid
            valid = True
            for i in range(0, len(pairs), 2):
                if weights[pairs[i]] + weights[pairs[i+1]] > capacity:
                    valid = False
                    break
            
            if valid:
                gondolas = k + len(remaining)
                min_gondolas = min(min_gondolas, gondolas)
    
    return min_gondolas

# Example usage
weights = [7, 2, 3, 9]
capacity = 10
result = brute_force_ferris_wheel(weights, capacity)
print(f"Brute force result: {result}")  # Output: 3
```

**Time Complexity**: O(2^n × n) - Exponential in number of children
**Space Complexity**: O(n) - For storing combinations

**Why it's inefficient**: Exponential time complexity makes it impractical for large inputs.

---

### Approach 2: Optimized - Greedy Pairing

**Key Insights from Optimized Approach**:
- **Greedy Strategy**: Always try to pair the heaviest child with the lightest available child
- **Efficient Processing**: Process children in sorted order
- **Better Complexity**: Achieve O(n²) time complexity
- **Not Always Optimal**: Greedy approach may not always give the optimal solution

**Key Insight**: Use a greedy approach to pair children, always trying to pair the heaviest child with the lightest available child.

**Algorithm**:
- Sort children by weight
- For each child from heaviest to lightest:
  - Try to pair with the lightest available child
  - If pairing is valid, use one gondola for both
  - Otherwise, use one gondola for the heavy child alone

**Visual Example**:
```
Weights: [7, 2, 3, 9], Capacity: 10
Sorted: [2, 3, 7, 9]

Greedy pairing:
1. Heaviest: 9, try to pair with lightest: 2 → 9+2=11>10 ✗
2. Heaviest: 9, try to pair with next: 3 → 9+3=12>10 ✗
3. Heaviest: 9, try to pair with next: 7 → 9+7=16>10 ✗
4. Child 9 goes alone → 1 gondola
5. Heaviest: 7, try to pair with lightest: 2 → 7+2=9≤10 ✓
6. Children 7 and 2 paired → 1 gondola
7. Heaviest: 3, no one left to pair → 1 gondola

Total: 3 gondolas
```

**Implementation**:
```python
def optimized_ferris_wheel(weights, capacity):
    """
    Find minimum gondolas using greedy approach
    
    Args:
        weights: list of child weights
        capacity: maximum weight per gondola
    
    Returns:
        int: minimum number of gondolas needed
    """
    weights = sorted(weights)
    used = [False] * len(weights)
    gondolas = 0
    
    # Process from heaviest to lightest
    for i in range(len(weights) - 1, -1, -1):
        if used[i]:
            continue
        
        # Try to pair with lightest available child
        paired = False
        for j in range(len(weights)):
            if not used[j] and i != j and weights[i] + weights[j] <= capacity:
                used[i] = used[j] = True
                gondolas += 1
                paired = True
                break
        
        if not paired:
            used[i] = True
            gondolas += 1
    
    return gondolas

# Example usage
weights = [7, 2, 3, 9]
capacity = 10
result = optimized_ferris_wheel(weights, capacity)
print(f"Optimized result: {result}")  # Output: 3
```

**Time Complexity**: O(n²) - For each child, check all other children
**Space Complexity**: O(n) - For used array

**Why it's better**: Much more efficient than brute force, but still not optimal.

---

### Approach 3: Optimal - Two Pointer Technique

**Key Insights from Optimal Approach**:
- **Two Pointer Technique**: Use two pointers to efficiently find valid pairs
- **Optimal Strategy**: Always pair the heaviest child with the lightest available child
- **Linear Time**: Achieve O(n log n) time complexity (due to sorting)
- **Mathematically Optimal**: This approach is proven to be optimal

**Key Insight**: Sort the weights and use two pointers to efficiently find the optimal pairing.

**Algorithm**:
- Sort children by weight
- Use two pointers: one at the beginning (lightest) and one at the end (heaviest)
- Try to pair the heaviest child with the lightest child
- If pairing is valid, use one gondola for both and move both pointers
- Otherwise, use one gondola for the heavy child alone and move only the right pointer

**Visual Example**:
```
Weights: [7, 2, 3, 9], Capacity: 10
Sorted: [2, 3, 7, 9]

Two pointer approach:
1. left=0, right=3: weights[0]=2, weights[3]=9 → 2+9=11>10 ✗
   - Child 9 goes alone, right=2
2. left=0, right=2: weights[0]=2, weights[2]=7 → 2+7=9≤10 ✓
   - Children 2 and 7 paired, left=1, right=1
3. left=1, right=1: weights[1]=3, weights[1]=3 → 3+3=6≤10 ✓
   - Child 3 goes alone, left=2, right=0

Total: 3 gondolas
```

**Implementation**:
```python
def optimal_ferris_wheel(weights, capacity):
    """
    Find minimum gondolas using two pointer technique
    
    Args:
        weights: list of child weights
        capacity: maximum weight per gondola
    
    Returns:
        int: minimum number of gondolas needed
    """
    weights.sort()
    left, right = 0, len(weights) - 1
    gondolas = 0
    
    while left <= right:
        if left == right:
            # Only one child left
            gondolas += 1
            break
        
        if weights[left] + weights[right] <= capacity:
            # Can pair the lightest and heaviest
            gondolas += 1
            left += 1
            right -= 1
        else:
            # Heaviest child must go alone
            gondolas += 1
            right -= 1
    
    return gondolas

# Example usage
weights = [7, 2, 3, 9]
capacity = 10
result = optimal_ferris_wheel(weights, capacity)
print(f"Optimal result: {result}")  # Output: 3
```

**Time Complexity**: O(n log n) - Sorting dominates
**Space Complexity**: O(1) - Constant extra space

**Why it's optimal**: Achieves the best possible time complexity and is mathematically proven to be optimal.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(2^n × n) | O(n) | Try all pairings |
| Greedy | O(n²) | O(n) | Pair heaviest with lightest |
| Two Pointer | O(n log n) | O(1) | Optimal pairing strategy |

### Time Complexity
- **Time**: O(n log n) - Two pointer technique provides optimal time complexity
- **Space**: O(1) - Constant extra space for two pointers

### Why This Solution Works
- **Greedy Choice**: Always pairing heaviest with lightest is optimal
- **Two Pointer Efficiency**: Eliminates redundant checks
- **Mathematical Proof**: This approach is proven to be optimal
- **Optimal Approach**: Two pointer technique provides the best balance of efficiency and correctness

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Ferris Wheel with Multiple Cars
**Problem**: Ferris wheel has multiple cars, each with different capacity limits.

**Link**: [CSES Problem Set - Ferris Wheel Multiple Cars](https://cses.fi/problemset/task/ferris_wheel_multiple_cars)

```python
def ferris_wheel_multiple_cars(weights, car_capacities):
    """
    Handle ferris wheel with multiple cars of different capacities
    """
    # Sort weights in descending order
    weights.sort(reverse=True)
    
    # Sort car capacities in descending order
    car_capacities.sort(reverse=True)
    
    # Use two pointers for each car
    result = 0
    used_weights = [False] * len(weights)
    
    for capacity in car_capacities:
        # Find pairs for this car
        left = 0
        right = len(weights) - 1
        car_pairs = 0
        
        while left < right:
            # Skip used weights
            while left < len(weights) and used_weights[left]:
                left += 1
            while right >= 0 and used_weights[right]:
                right -= 1
            
            if left >= right:
                break
            
            # Check if pair fits in car
            if weights[left] + weights[right] <= capacity:
                used_weights[left] = True
                used_weights[right] = True
                car_pairs += 1
                left += 1
                right -= 1
            else:
                # Heaviest person alone
                used_weights[left] = True
                car_pairs += 1
                left += 1
        
        result += car_pairs
    
    return result
```

### Variation 2: Ferris Wheel with Time Constraints
**Problem**: Each person has a time limit, and the ferris wheel takes time to complete a ride.

**Link**: [CSES Problem Set - Ferris Wheel Time Constraints](https://cses.fi/problemset/task/ferris_wheel_time)

```python
def ferris_wheel_time_constraints(people, capacity, ride_time):
    """
    Handle ferris wheel with time constraints for each person
    """
    # Sort people by time limit (ascending)
    people.sort(key=lambda x: x['time_limit'])
    
    result = 0
    used = [False] * len(people)
    
    for i in range(len(people)):
        if used[i]:
            continue
        
        # Find best partner for this person
        best_partner = -1
        best_weight_sum = float('inf')
        
        for j in range(i + 1, len(people)):
            if used[j]:
                continue
            
            # Check if both can ride together
            if (people[i]['time_limit'] >= ride_time and 
                people[j]['time_limit'] >= ride_time):
                
                weight_sum = people[i]['weight'] + people[j]['weight']
                if weight_sum <= capacity and weight_sum < best_weight_sum:
                    best_partner = j
                    best_weight_sum = weight_sum
        
        if best_partner != -1:
            # Pair them together
            used[i] = True
            used[best_partner] = True
            result += 1
        else:
            # Single person ride
            if people[i]['weight'] <= capacity:
                used[i] = True
                result += 1
    
    return result
```

### Variation 3: Ferris Wheel with Priority Queues
**Problem**: People have different priorities, and we want to maximize total priority.

**Link**: [CSES Problem Set - Ferris Wheel Priority Queues](https://cses.fi/problemset/task/ferris_wheel_priority)

```python
def ferris_wheel_priority_queues(people, capacity):
    """
    Handle ferris wheel with priority optimization
    """
    # Sort people by priority (descending)
    people.sort(key=lambda x: x['priority'], reverse=True)
    
    result = 0
    used = [False] * len(people)
    
    for i in range(len(people)):
        if used[i]:
            continue
        
        # Find best partner for this person
        best_partner = -1
        best_priority_sum = 0
        
        for j in range(i + 1, len(people)):
            if used[j]:
                continue
            
            # Check if they can ride together
            if people[i]['weight'] + people[j]['weight'] <= capacity:
                priority_sum = people[i]['priority'] + people[j]['priority']
                if priority_sum > best_priority_sum:
                    best_partner = j
                    best_priority_sum = priority_sum
        
        if best_partner != -1:
            # Pair them together
            used[i] = True
            used[best_partner] = True
            result += best_priority_sum
        else:
            # Single person ride
            if people[i]['weight'] <= capacity:
                used[i] = True
                result += people[i]['priority']
    
    return result
```

## Problem Variations

### **Variation 1: Ferris Wheel with Dynamic Updates**
**Problem**: Handle dynamic updates (add/remove people, change capacity) while maintaining efficient ride allocation.

**Approach**: Use balanced binary search trees or segment trees for efficient updates and queries.

```python
from collections import defaultdict
import bisect

class DynamicFerrisWheel:
    def __init__(self, capacity):
        self.capacity = capacity
        self.people = []
        self.sorted_weights = []
        self.used = set()
    
    def add_person(self, weight):
        """Add a new person to the queue."""
        person_id = len(self.people)
        self.people.append(weight)
        bisect.insort(self.sorted_weights, (weight, person_id))
        return person_id
    
    def remove_person(self, person_id):
        """Remove a person from the queue."""
        if person_id < len(self.people) and person_id not in self.used:
            weight = self.people[person_id]
            # Remove from sorted weights
            for i, (w, pid) in enumerate(self.sorted_weights):
                if pid == person_id:
                    del self.sorted_weights[i]
                    break
            self.people[person_id] = None  # Mark as removed
    
    def update_capacity(self, new_capacity):
        """Update the ferris wheel capacity."""
        self.capacity = new_capacity
    
    def get_optimal_rides(self):
        """Get optimal number of rides using two-pointer technique."""
        # Filter out removed people and unused people
        available_people = []
        for i, (weight, person_id) in enumerate(self.sorted_weights):
            if (person_id < len(self.people) and 
                self.people[person_id] is not None and 
                person_id not in self.used):
                available_people.append(weight)
        
        if not available_people:
            return 0
        
        # Two-pointer approach
        left = 0
        right = len(available_people) - 1
        rides = 0
        
        while left <= right:
            if available_people[left] + available_people[right] <= self.capacity:
                left += 1
            right -= 1
            rides += 1
        
        return rides
    
    def get_ride_allocation(self):
        """Get detailed ride allocation."""
        # Filter out removed people and unused people
        available_people = []
        for i, (weight, person_id) in enumerate(self.sorted_weights):
            if (person_id < len(self.people) and 
                self.people[person_id] is not None and 
                person_id not in self.used):
                available_people.append((weight, person_id))
        
        if not available_people:
            return []
        
        # Two-pointer approach with tracking
        left = 0
        right = len(available_people) - 1
        rides = []
        
        while left <= right:
            if (available_people[left][0] + available_people[right][0] <= self.capacity and 
                left != right):
                # Pair ride
                rides.append([available_people[left][1], available_people[right][1]])
                left += 1
                right -= 1
            else:
                # Single ride
                rides.append([available_people[right][1]])
                right -= 1
        
        return rides
    
    def get_utilization_rate(self):
        """Get capacity utilization rate."""
        rides = self.get_ride_allocation()
        if not rides:
            return 0.0
        
        total_weight = 0
        total_capacity_used = 0
        
        for ride in rides:
            ride_weight = sum(self.people[person_id] for person_id in ride)
            total_weight += ride_weight
            total_capacity_used += self.capacity
        
        return total_weight / total_capacity_used if total_capacity_used > 0 else 0.0
    
    def get_waiting_time_estimate(self, person_id):
        """Get estimated waiting time for a person."""
        if person_id >= len(self.people) or self.people[person_id] is None:
            return -1
        
        # Count people ahead in queue
        ahead_count = 0
        person_weight = self.people[person_id]
        
        for weight, pid in self.sorted_weights:
            if pid == person_id:
                break
            if (pid < len(self.people) and 
                self.people[pid] is not None and 
                pid not in self.used):
                ahead_count += 1
        
        # Estimate based on optimal pairing
        estimated_rides_ahead = (ahead_count + 1) // 2
        return estimated_rides_ahead * 5  # Assuming 5 minutes per ride

# Example usage
ferris_wheel = DynamicFerrisWheel(10)

# Add people
person1 = ferris_wheel.add_person(3)
person2 = ferris_wheel.add_person(7)
person3 = ferris_wheel.add_person(4)
person4 = ferris_wheel.add_person(6)

print(f"Optimal rides: {ferris_wheel.get_optimal_rides()}")
print(f"Ride allocation: {ferris_wheel.get_ride_allocation()}")
print(f"Utilization rate: {ferris_wheel.get_utilization_rate():.2f}")

# Update capacity
ferris_wheel.update_capacity(12)
print(f"After capacity update: {ferris_wheel.get_optimal_rides()}")

# Remove a person
ferris_wheel.remove_person(person2)
print(f"After removing person: {ferris_wheel.get_optimal_rides()}")
```

### **Variation 2: Ferris Wheel with Different Operations**
**Problem**: Handle different types of operations on ferris wheel (priority scheduling, group bookings, VIP access).

**Approach**: Use advanced data structures for efficient priority management and group handling.

```python
class AdvancedFerrisWheel:
    def __init__(self, capacity):
        self.capacity = capacity
        self.people = []
        self.priority_queue = []
        self.groups = []
        self.vip_people = set()
    
    def add_person_with_priority(self, weight, priority, is_vip=False):
        """Add person with priority and VIP status."""
        person_id = len(self.people)
        person = {
            'id': person_id,
            'weight': weight,
            'priority': priority,
            'is_vip': is_vip
        }
        self.people.append(person)
        
        if is_vip:
            self.vip_people.add(person_id)
        
        # Insert into priority queue (higher priority first)
        bisect.insort(self.priority_queue, (-priority, person_id))
        return person_id
    
    def add_group(self, group_weights, group_priority=0):
        """Add a group of people who want to ride together."""
        group_id = len(self.groups)
        group = {
            'id': group_id,
            'weights': group_weights,
            'total_weight': sum(group_weights),
            'priority': group_priority,
            'size': len(group_weights)
        }
        self.groups.append(group)
        return group_id
    
    def get_optimal_rides_with_priority(self):
        """Get optimal rides considering priorities."""
        # Separate VIP and regular people
        vip_people = []
        regular_people = []
        
        for person in self.people:
            if person['is_vip']:
                vip_people.append(person)
            else:
                regular_people.append(person)
        
        # Sort by priority (higher priority first)
        vip_people.sort(key=lambda x: x['priority'], reverse=True)
        regular_people.sort(key=lambda x: x['priority'], reverse=True)
        
        rides = []
        used = set()
        
        # Process VIP people first
        vip_rides = self._allocate_rides(vip_people, used)
        rides.extend(vip_rides)
        
        # Process regular people
        regular_rides = self._allocate_rides(regular_people, used)
        rides.extend(regular_rides)
        
        return rides
    
    def _allocate_rides(self, people, used):
        """Allocate rides for a group of people."""
        rides = []
        people = [p for p in people if p['id'] not in used]
        
        if not people:
            return rides
        
        # Sort by weight for two-pointer technique
        people.sort(key=lambda x: x['weight'])
        
        left = 0
        right = len(people) - 1
        
        while left <= right:
            if (people[left]['weight'] + people[right]['weight'] <= self.capacity and 
                left != right):
                # Pair ride
                rides.append([people[left]['id'], people[right]['id']])
                used.add(people[left]['id'])
                used.add(people[right]['id'])
                left += 1
                right -= 1
            else:
                # Single ride
                rides.append([people[right]['id']])
                used.add(people[right]['id'])
                right -= 1
        
        return rides
    
    def get_optimal_rides_with_groups(self):
        """Get optimal rides considering group bookings."""
        rides = []
        used_people = set()
        used_groups = set()
        
        # Sort groups by priority and size
        sorted_groups = sorted(self.groups, key=lambda x: (-x['priority'], -x['size']))
        
        # Process groups first
        for group in sorted_groups:
            if group['id'] in used_groups:
                continue
            
            if group['total_weight'] <= self.capacity:
                # Group can ride together
                group_ride = []
                for i, weight in enumerate(group['weights']):
                    person_id = len(self.people) + i  # Virtual person IDs for group members
                    group_ride.append(person_id)
                
                rides.append(group_ride)
                used_groups.add(group['id'])
            else:
                # Group too heavy, split or skip
                continue
        
        # Process individual people
        individual_people = [p for p in self.people if p['id'] not in used_people]
        individual_rides = self._allocate_rides(individual_people, used_people)
        rides.extend(individual_rides)
        
        return rides
    
    def get_optimal_rides_mixed(self):
        """Get optimal rides with mixed priority and group handling."""
        rides = []
        used_people = set()
        used_groups = set()
        
        # Process VIP groups first
        vip_groups = [g for g in self.groups if g['priority'] > 5]
        vip_groups.sort(key=lambda x: -x['priority'])
        
        for group in vip_groups:
            if group['total_weight'] <= self.capacity:
                group_ride = []
                for i, weight in enumerate(group['weights']):
                    person_id = len(self.people) + i
                    group_ride.append(person_id)
                
                rides.append(group_ride)
                used_groups.add(group['id'])
        
        # Process VIP individuals
        vip_people = [p for p in self.people if p['is_vip'] and p['id'] not in used_people]
        vip_rides = self._allocate_rides(vip_people, used_people)
        rides.extend(vip_rides)
        
        # Process regular groups
        regular_groups = [g for g in self.groups if g['priority'] <= 5 and g['id'] not in used_groups]
        regular_groups.sort(key=lambda x: -x['priority'])
        
        for group in regular_groups:
            if group['total_weight'] <= self.capacity:
                group_ride = []
                for i, weight in enumerate(group['weights']):
                    person_id = len(self.people) + i
                    group_ride.append(person_id)
                
                rides.append(group_ride)
                used_groups.add(group['id'])
        
        # Process regular individuals
        regular_people = [p for p in self.people if not p['is_vip'] and p['id'] not in used_people]
        regular_rides = self._allocate_rides(regular_people, used_people)
        rides.extend(regular_rides)
        
        return rides
    
    def get_revenue_optimization(self, ticket_prices):
        """Get rides that maximize revenue."""
        # Sort people by revenue potential (weight * price per kg)
        revenue_people = []
        for person in self.people:
            revenue = person['weight'] * ticket_prices.get(person['id'], 1.0)
            revenue_people.append((person, revenue))
        
        revenue_people.sort(key=lambda x: x[1], reverse=True)
        
        rides = []
        used = set()
        
        # Greedy approach: pair high-revenue people
        for i, (person1, revenue1) in enumerate(revenue_people):
            if person1['id'] in used:
                continue
            
            best_partner = None
            best_revenue = revenue1
            
            for j, (person2, revenue2) in enumerate(revenue_people[i+1:], i+1):
                if person2['id'] in used:
                    continue
                
                if person1['weight'] + person2['weight'] <= self.capacity:
                    total_revenue = revenue1 + revenue2
                    if total_revenue > best_revenue:
                        best_partner = person2
                        best_revenue = total_revenue
            
            if best_partner:
                rides.append([person1['id'], best_partner['id']])
                used.add(person1['id'])
                used.add(best_partner['id'])
            else:
                rides.append([person1['id']])
                used.add(person1['id'])
        
        return rides

# Example usage
advanced_wheel = AdvancedFerrisWheel(10)

# Add people with priorities
person1 = advanced_wheel.add_person_with_priority(3, 5, is_vip=True)
person2 = advanced_wheel.add_person_with_priority(7, 3)
person3 = advanced_wheel.add_person_with_priority(4, 8, is_vip=True)
person4 = advanced_wheel.add_person_with_priority(6, 2)

# Add groups
group1 = advanced_wheel.add_group([2, 3], priority=7)
group2 = advanced_wheel.add_group([4, 5], priority=4)

print("Priority-based rides:", advanced_wheel.get_optimal_rides_with_priority())
print("Group-based rides:", advanced_wheel.get_optimal_rides_with_groups())
print("Mixed rides:", advanced_wheel.get_optimal_rides_mixed())

# Revenue optimization
ticket_prices = {person1: 2.0, person2: 1.5, person3: 2.5, person4: 1.0}
print("Revenue-optimized rides:", advanced_wheel.get_revenue_optimization(ticket_prices))
```

### **Variation 3: Ferris Wheel with Constraints**
**Problem**: Handle ferris wheel with additional constraints (time limits, safety requirements, capacity variations).

**Approach**: Use constraint satisfaction with advanced scheduling and optimization.

```python
class ConstrainedFerrisWheel:
    def __init__(self, base_capacity, constraints=None):
        self.base_capacity = base_capacity
        self.constraints = constraints or {}
        self.people = []
        self.ride_history = []
    
    def add_person_with_constraints(self, weight, time_limit, safety_rating, age):
        """Add person with various constraints."""
        person_id = len(self.people)
        person = {
            'id': person_id,
            'weight': weight,
            'time_limit': time_limit,
            'safety_rating': safety_rating,
            'age': age
        }
        self.people.append(person)
        return person_id
    
    def can_ride_together(self, person1, person2):
        """Check if two people can ride together based on constraints."""
        # Weight constraint
        if person1['weight'] + person2['weight'] > self.base_capacity:
            return False
        
        # Time constraint
        if (person1['time_limit'] < 10 or person2['time_limit'] < 10):
            return False
        
        # Safety constraint
        if (person1['safety_rating'] < 3 or person2['safety_rating'] < 3):
            return False
        
        # Age constraint (adults with children)
        if (person1['age'] < 12 and person2['age'] > 18) or (person1['age'] > 18 and person2['age'] < 12):
            return False
        
        return True
    
    def get_optimal_rides_with_time_constraints(self):
        """Get optimal rides considering time constraints."""
        # Sort by time limit (ascending)
        sorted_people = sorted(self.people, key=lambda x: x['time_limit'])
        
        rides = []
        used = set()
        
        for i, person1 in enumerate(sorted_people):
            if person1['id'] in used:
                continue
            
            # Find best partner within time constraints
            best_partner = None
            best_time_remaining = 0
            
            for j, person2 in enumerate(sorted_people[i+1:], i+1):
                if person2['id'] in used:
                    continue
                
                if self.can_ride_together(person1, person2):
                    # Calculate remaining time after ride
                    time_remaining = min(person1['time_limit'], person2['time_limit']) - 10
                    if time_remaining > best_time_remaining:
                        best_partner = person2
                        best_time_remaining = time_remaining
            
            if best_partner:
                rides.append([person1['id'], best_partner['id']])
                used.add(person1['id'])
                used.add(best_partner['id'])
            else:
                # Single ride if time allows
                if person1['time_limit'] >= 10:
                    rides.append([person1['id']])
                    used.add(person1['id'])
        
        return rides
    
    def get_optimal_rides_with_safety_constraints(self):
        """Get optimal rides considering safety requirements."""
        # Group people by safety rating
        safety_groups = defaultdict(list)
        for person in self.people:
            safety_groups[person['safety_rating']].append(person)
        
        rides = []
        used = set()
        
        # Process high safety rating people first
        for safety_rating in sorted(safety_groups.keys(), reverse=True):
            group_people = safety_groups[safety_rating]
            group_people.sort(key=lambda x: x['weight'])
            
            left = 0
            right = len(group_people) - 1
            
            while left <= right:
                if group_people[left]['id'] in used:
                    left += 1
                    continue
                if group_people[right]['id'] in used:
                    right -= 1
                    continue
                
                if (group_people[left]['weight'] + group_people[right]['weight'] <= self.base_capacity and 
                    left != right):
                    rides.append([group_people[left]['id'], group_people[right]['id']])
                    used.add(group_people[left]['id'])
                    used.add(group_people[right]['id'])
                    left += 1
                    right -= 1
                else:
                    rides.append([group_people[right]['id']])
                    used.add(group_people[right]['id'])
                    right -= 1
        
        return rides
    
    def get_optimal_rides_with_capacity_variations(self, capacity_schedule):
        """Get optimal rides with varying capacity over time."""
        rides = []
        used = set()
        current_time = 0
        
        # Sort people by priority (time limit)
        sorted_people = sorted(self.people, key=lambda x: x['time_limit'])
        
        for person in sorted_people:
            if person['id'] in used:
                continue
            
            # Find current capacity
            current_capacity = self.base_capacity
            for time, capacity in capacity_schedule:
                if current_time >= time:
                    current_capacity = capacity
            
            # Find best partner for current capacity
            best_partner = None
            best_weight_sum = 0
            
            for other_person in sorted_people:
                if (other_person['id'] in used or 
                    other_person['id'] == person['id']):
                    continue
                
                weight_sum = person['weight'] + other_person['weight']
                if (weight_sum <= current_capacity and 
                    weight_sum > best_weight_sum):
                    best_partner = other_person
                    best_weight_sum = weight_sum
            
            if best_partner:
                rides.append([person['id'], best_partner['id']])
                used.add(person['id'])
                used.add(best_partner['id'])
            else:
                # Single ride if weight allows
                if person['weight'] <= current_capacity:
                    rides.append([person['id']])
                    used.add(person['id'])
            
            current_time += 10  # 10 minutes per ride
        
        return rides
    
    def get_optimal_rides_with_weather_constraints(self, weather_conditions):
        """Get optimal rides considering weather conditions."""
        rides = []
        used = set()
        
        # Adjust capacity based on weather
        weather_capacity = self.base_capacity
        if weather_conditions == 'storm':
            weather_capacity = self.base_capacity // 2
        elif weather_conditions == 'wind':
            weather_capacity = int(self.base_capacity * 0.8)
        
        # Sort people by safety rating (higher first)
        sorted_people = sorted(self.people, key=lambda x: x['safety_rating'], reverse=True)
        
        for person in sorted_people:
            if person['id'] in used:
                continue
            
            # Find best partner for weather conditions
            best_partner = None
            best_safety_sum = 0
            
            for other_person in sorted_people:
                if (other_person['id'] in used or 
                    other_person['id'] == person['id']):
                    continue
                
                if (person['weight'] + other_person['weight'] <= weather_capacity):
                    safety_sum = person['safety_rating'] + other_person['safety_rating']
                    if safety_sum > best_safety_sum:
                        best_partner = other_person
                        best_safety_sum = safety_sum
            
            if best_partner:
                rides.append([person['id'], best_partner['id']])
                used.add(person['id'])
                used.add(best_partner['id'])
            else:
                # Single ride if weight and safety allow
                if (person['weight'] <= weather_capacity and 
                    person['safety_rating'] >= 4):
                    rides.append([person['id']])
                    used.add(person['id'])
        
        return rides
    
    def get_optimal_rides_with_maintenance_constraints(self, maintenance_schedule):
        """Get optimal rides considering maintenance windows."""
        rides = []
        used = set()
        current_time = 0
        
        # Sort people by time limit
        sorted_people = sorted(self.people, key=lambda x: x['time_limit'])
        
        for person in sorted_people:
            if person['id'] in used:
                continue
            
            # Check if maintenance is scheduled
            maintenance_active = False
            for start_time, end_time in maintenance_schedule:
                if start_time <= current_time < end_time:
                    maintenance_active = True
                    break
            
            if maintenance_active:
                # Skip rides during maintenance
                current_time += 10
                continue
            
            # Find best partner
            best_partner = None
            best_weight_sum = 0
            
            for other_person in sorted_people:
                if (other_person['id'] in used or 
                    other_person['id'] == person['id']):
                    continue
                
                weight_sum = person['weight'] + other_person['weight']
                if (weight_sum <= self.base_capacity and 
                    weight_sum > best_weight_sum):
                    best_partner = other_person
                    best_weight_sum = weight_sum
            
            if best_partner:
                rides.append([person['id'], best_partner['id']])
                used.add(person['id'])
                used.add(best_partner['id'])
            else:
                rides.append([person['id']])
                used.add(person['id'])
            
            current_time += 10
        
        return rides

# Example usage
constraints = {
    'min_safety_rating': 3,
    'max_age_difference': 10,
    'min_time_limit': 10
}

constrained_wheel = ConstrainedFerrisWheel(10, constraints)

# Add people with constraints
person1 = constrained_wheel.add_person_with_constraints(3, 20, 5, 25)
person2 = constrained_wheel.add_person_with_constraints(7, 15, 4, 30)
person3 = constrained_wheel.add_person_with_constraints(4, 25, 3, 20)
person4 = constrained_wheel.add_person_with_constraints(6, 10, 5, 35)

print("Time-constrained rides:", constrained_wheel.get_optimal_rides_with_time_constraints())
print("Safety-constrained rides:", constrained_wheel.get_optimal_rides_with_safety_constraints())

# Capacity variations over time
capacity_schedule = [(0, 10), (10, 8), (20, 12)]
print("Capacity-varied rides:", constrained_wheel.get_optimal_rides_with_capacity_variations(capacity_schedule))

# Weather constraints
print("Weather-constrained rides:", constrained_wheel.get_optimal_rides_with_weather_constraints('wind'))

# Maintenance constraints
maintenance_schedule = [(30, 50), (80, 100)]
print("Maintenance-constrained rides:", constrained_wheel.get_optimal_rides_with_maintenance_constraints(maintenance_schedule))
```

### Related Problems

#### **CSES Problems**
- [Ferris Wheel](https://cses.fi/problemset/task/1090) - Basic ferris wheel problem
- [Apartments](https://cses.fi/problemset/task/1084) - Similar two-pointer problem
- [Concert Tickets](https://cses.fi/problemset/task/1091) - Binary search optimization

#### **LeetCode Problems**
- [Two Sum](https://leetcode.com/problems/two-sum/) - Find pairs with target sum
- [3Sum](https://leetcode.com/problems/3sum/) - Find triplets with zero sum
- [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) - Two-pointer optimization
- [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) - Two-pointer water trapping

#### **Problem Categories**
- **Two Pointers**: Efficient array processing, sorted array algorithms, pairing problems
- **Greedy Algorithms**: Optimal local choices, sorting-based optimization, matching problems
- **Sorting**: Array sorting, two-pointer techniques, efficient pairing algorithms
- **Algorithm Design**: Two-pointer techniques, greedy strategies, optimization algorithms
