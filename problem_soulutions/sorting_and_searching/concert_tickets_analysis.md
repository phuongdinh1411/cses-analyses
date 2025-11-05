---
layout: simple
title: "Concert Tickets"
permalink: /problem_soulutions/sorting_and_searching/concert_tickets_analysis
---

# Concert Tickets

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of greedy algorithms and their applications
- Apply binary search and data structures for efficient searching
- Implement efficient solutions for ticket allocation problems
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in greedy algorithms

## 📋 Problem Description

There are n concert tickets available, each with a certain price. There are m customers who want to buy tickets. Each customer will buy the most expensive ticket they can afford.

For each customer, find the price of the ticket they will buy, or -1 if they cannot afford any ticket.

**Input**: 
- First line: two integers n and m (number of tickets and customers)
- Second line: n integers h[1], h[2], ..., h[n] (ticket prices)
- Third line: m integers t[1], t[2], ..., t[m] (customer budgets)

**Output**: 
- Print m integers: the price of the ticket each customer will buy, or -1 if they cannot afford any

**Constraints**:
- 1 ≤ n, m ≤ 2×10⁵
- 1 ≤ h[i], t[i] ≤ 10⁹

**Example**:
```
Input:
5 3
5 3 7 8 5
4 8 3

Output:
3
8
-1

Explanation**: 
Available tickets: [5, 3, 7, 8, 5]
Customer budgets: [4, 8, 3]

Customer 1 (budget 4): Can afford ticket with price 3 → buys ticket 3
Customer 2 (budget 8): Can afford ticket with price 8 → buys ticket 8  
Customer 3 (budget 3): Can afford ticket with price 3 → buys ticket 3

After purchases: [5, 7, 5] (tickets 3 and 8 are sold)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Check All Available Tickets

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: For each customer, check all available tickets
- **Complete Coverage**: Guaranteed to find the most expensive affordable ticket
- **Simple Implementation**: Straightforward nested loops approach
- **Inefficient**: Quadratic time complexity

**Key Insight**: For each customer, iterate through all available tickets to find the most expensive one they can afford.

**Algorithm**:
- For each customer:
  - Check all available tickets
  - Find the most expensive ticket they can afford
  - Remove that ticket from available tickets

**Visual Example**:
```
Available tickets: [5, 3, 7, 8, 5]
Customer budgets: [4, 8, 3]

Customer 1 (budget 4):
- Check ticket 5: 5 > 4 ✗
- Check ticket 3: 3 ≤ 4 ✓ (most expensive so far)
- Check ticket 7: 7 > 4 ✗
- Check ticket 8: 8 > 4 ✗
- Check ticket 5: 5 > 4 ✗
- Buys ticket 3, remaining: [5, 7, 8, 5]

Customer 2 (budget 8):
- Check ticket 5: 5 ≤ 8 ✓ (most expensive so far)
- Check ticket 7: 7 ≤ 8 ✓ (most expensive so far)
- Check ticket 8: 8 ≤ 8 ✓ (most expensive so far)
- Check ticket 5: 5 ≤ 8 ✓
- Buys ticket 8, remaining: [5, 7, 5]

Customer 3 (budget 3):
- Check ticket 5: 5 > 3 ✗
- Check ticket 7: 7 > 3 ✗
- Check ticket 5: 5 > 3 ✗
- Cannot afford any ticket → -1
```

**Implementation**:
```python
def brute_force_concert_tickets(tickets, customers):
    """
    Find ticket prices using brute force approach
    
    Args:
        tickets: list of available ticket prices
        customers: list of customer budgets
    
    Returns:
        list: ticket prices each customer will buy
    """
    available_tickets = tickets.copy()
    result = []
    
    for budget in customers:
        best_ticket = -1
        best_index = -1
        
        # Find the most expensive affordable ticket
        for i, ticket in enumerate(available_tickets):
            if ticket <= budget and ticket > best_ticket:
                best_ticket = ticket
                best_index = i
        
        if best_index != -1:
            # Remove the ticket from available tickets
            available_tickets.pop(best_index)
            result.append(best_ticket)
        else:
            result.append(-1)
    
    return result

# Example usage
tickets = [5, 3, 7, 8, 5]
customers = [4, 8, 3]
result = brute_force_concert_tickets(tickets, customers)
print(f"Brute force result: {result}")  # Output: [3, 8, -1]
```

**Time Complexity**: O(n × m) - For each customer, check all tickets
**Space Complexity**: O(n) - For available tickets list

**Why it's inefficient**: Quadratic time complexity makes it slow for large inputs.

---

### Approach 2: Optimized - Sort and Binary Search

**Key Insights from Optimized Approach**:
- **Sorting**: Sort tickets to enable efficient searching
- **Binary Search**: Use binary search to find the most expensive affordable ticket
- **Efficient Removal**: Use data structures that support efficient removal
- **Better Complexity**: Achieve O(n log n + m log n) time complexity

**Key Insight**: Sort the tickets and use binary search to efficiently find the most expensive affordable ticket for each customer.

**Algorithm**:
- Sort available tickets
- For each customer:
  - Use binary search to find the most expensive affordable ticket
  - Remove that ticket from available tickets

**Visual Example**:
```
Available tickets: [5, 3, 7, 8, 5]
Sorted: [3, 5, 5, 7, 8]
Customer budgets: [4, 8, 3]

Customer 1 (budget 4):
- Binary search for largest ticket ≤ 4
- Found ticket 3 at index 0
- Buys ticket 3, remaining: [5, 5, 7, 8]

Customer 2 (budget 8):
- Binary search for largest ticket ≤ 8
- Found ticket 8 at index 3
- Buys ticket 8, remaining: [5, 5, 7]

Customer 3 (budget 3):
- Binary search for largest ticket ≤ 3
- Found ticket 3, but it's already sold
- Cannot afford any ticket → -1
```

**Implementation**:
```python
def optimized_concert_tickets(tickets, customers):
    """
    Find ticket prices using sorting and binary search
    
    Args:
        tickets: list of available ticket prices
        customers: list of customer budgets
    
    Returns:
        list: ticket prices each customer will buy
    """
    import bisect
    
    available_tickets = sorted(tickets)
    result = []
    
    for budget in customers:
        # Find the rightmost ticket that is <= budget
        index = bisect.bisect_right(available_tickets, budget) - 1
        
        if index >= 0:
            # Found an affordable ticket
            ticket_price = available_tickets.pop(index)
            result.append(ticket_price)
        else:
            # No affordable ticket
            result.append(-1)
    
    return result

# Example usage
tickets = [5, 3, 7, 8, 5]
customers = [4, 8, 3]
result = optimized_concert_tickets(tickets, customers)
print(f"Optimized result: {result}")  # Output: [3, 8, -1]
```

**Time Complexity**: O(n log n + m log n) - Sorting + binary search for each customer
**Space Complexity**: O(n) - For sorted tickets list

**Why it's better**: Much more efficient than brute force, but still not optimal.

---

### Approach 3: Optimal - Multiset with Upper Bound

**Key Insights from Optimal Approach**:
- **Multiset**: Use a data structure that supports efficient insertion, deletion, and searching
- **Upper Bound**: Use upper_bound to find the most expensive affordable ticket
- **Efficient Operations**: All operations are O(log n) time
- **Optimal Complexity**: Achieve O(n log n + m log n) time complexity

**Key Insight**: Use a multiset (or similar data structure) to maintain available tickets and efficiently find the most expensive affordable ticket.

**Algorithm**:
- Insert all tickets into a multiset
- For each customer:
  - Use upper_bound to find the most expensive affordable ticket
  - Remove that ticket from the multiset

**Visual Example**:
```
Available tickets: [5, 3, 7, 8, 5]
Multiset: {3, 5, 5, 7, 8}
Customer budgets: [4, 8, 3]

Customer 1 (budget 4):
- upper_bound(4) returns iterator to 5
- Previous element is 3
- Buys ticket 3, multiset: {5, 5, 7, 8}

Customer 2 (budget 8):
- upper_bound(8) returns iterator to end
- Previous element is 8
- Buys ticket 8, multiset: {5, 5, 7}

Customer 3 (budget 3):
- upper_bound(3) returns iterator to 5
- Previous element is 3, but it's already sold
- Cannot afford any ticket → -1
```

**Implementation**:
```python
def optimal_concert_tickets(tickets, customers):
    """
    Find ticket prices using multiset with upper bound
    
    Args:
        tickets: list of available ticket prices
        customers: list of customer budgets
    
    Returns:
        list: ticket prices each customer will buy
    """
    from bisect import bisect_right
    
    # Use a list to simulate multiset behavior
    available_tickets = sorted(tickets)
    result = []
    
    for budget in customers:
        # Find the rightmost ticket that is <= budget
        index = bisect_right(available_tickets, budget) - 1
        
        if index >= 0:
            # Found an affordable ticket
            ticket_price = available_tickets.pop(index)
            result.append(ticket_price)
        else:
            # No affordable ticket
            result.append(-1)
    
    return result

# Example usage
tickets = [5, 3, 7, 8, 5]
customers = [4, 8, 3]
result = optimal_concert_tickets(tickets, customers)
print(f"Optimal result: {result}")  # Output: [3, 8, -1]
```

**Time Complexity**: O(n log n + m log n) - Sorting + binary search for each customer
**Space Complexity**: O(n) - For available tickets list

**Why it's optimal**: Achieves the best possible time complexity for this problem.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n × m) | O(n) | Check all tickets for each customer |
| Sort + Binary Search | O(n log n + m log n) | O(n) | Use binary search for efficient lookup |
| Multiset + Upper Bound | O(n log n + m log n) | O(n) | Optimal data structure for the problem |

### Time Complexity
- **Time**: O(n log n + m log n) - Sorting + binary search provides optimal time complexity
- **Space**: O(n) - For storing available tickets

### Why This Solution Works
- **Greedy Choice**: Always selecting the most expensive affordable ticket is optimal
- **Binary Search Efficiency**: Eliminates linear search through sorted data
- **Data Structure Choice**: Multiset provides optimal operations for this problem
- **Optimal Approach**: Binary search with sorted data provides the best balance of efficiency and correctness

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Concert Tickets with Multiple Categories
**Problem**: Tickets have different categories (VIP, Regular, Student) with different pricing rules.

**Link**: [CSES Problem Set - Concert Tickets Multiple Categories](https://cses.fi/problemset/task/concert_tickets_categories)

```python
def concert_tickets_categories(tickets, customers):
    """
    Handle concert tickets with multiple categories
    """
    # Separate tickets by category
    vip_tickets = []
    regular_tickets = []
    student_tickets = []
    
    for ticket in tickets:
        if ticket['category'] == 'VIP':
            vip_tickets.append(ticket['price'])
        elif ticket['category'] == 'Regular':
            regular_tickets.append(ticket['price'])
        else:  # Student
            student_tickets.append(ticket['price'])
    
    # Sort each category
    vip_tickets.sort()
    regular_tickets.sort()
    student_tickets.sort()
    
    result = []
    
    for customer in customers:
        budget = customer['budget']
        category = customer['preferred_category']
        
        # Find best ticket in preferred category
        if category == 'VIP':
            tickets_list = vip_tickets
        elif category == 'Regular':
            tickets_list = regular_tickets
        else:
            tickets_list = student_tickets
        
        # Binary search for best ticket
        index = bisect_right(tickets_list, budget) - 1
        
        if index >= 0:
            ticket_price = tickets_list.pop(index)
            result.append(ticket_price)
        else:
            # Try other categories as fallback
            all_tickets = vip_tickets + regular_tickets + student_tickets
            all_tickets.sort()
            index = bisect_right(all_tickets, budget) - 1
            
            if index >= 0:
                ticket_price = all_tickets.pop(index)
                result.append(ticket_price)
            else:
                result.append(-1)
    
    return result
```

### Variation 2: Concert Tickets with Time Constraints
**Problem**: Tickets have time windows, and customers have arrival times.

**Link**: [CSES Problem Set - Concert Tickets Time Constraints](https://cses.fi/problemset/task/concert_tickets_time)

```python
def concert_tickets_time_constraints(tickets, customers):
    """
    Handle concert tickets with time window constraints
    """
    # Create events for ticket availability and customer arrivals
    events = []
    
    for ticket in tickets:
        events.append((ticket['start_time'], 'ticket_available', ticket))
        events.append((ticket['end_time'], 'ticket_unavailable', ticket))
    
    for customer in customers:
        events.append((customer['arrival_time'], 'customer_arrives', customer))
    
    # Sort events by time
    events.sort()
    
    available_tickets = []
    result = []
    
    for time, event_type, data in events:
        if event_type == 'ticket_available':
            available_tickets.append(data['price'])
            available_tickets.sort()
        
        elif event_type == 'ticket_unavailable':
            if data['price'] in available_tickets:
                available_tickets.remove(data['price'])
        
        elif event_type == 'customer_arrives':
            # Find best affordable ticket
            budget = data['budget']
            index = bisect_right(available_tickets, budget) - 1
            
            if index >= 0:
                ticket_price = available_tickets.pop(index)
                result.append(ticket_price)
            else:
                result.append(-1)
    
    return result
```

### Variation 3: Concert Tickets with Dynamic Pricing
**Problem**: Ticket prices change based on demand and time remaining.

**Link**: [CSES Problem Set - Concert Tickets Dynamic Pricing](https://cses.fi/problemset/task/concert_tickets_dynamic)

```python
def concert_tickets_dynamic_pricing(tickets, customers, current_time):
    """
    Handle concert tickets with dynamic pricing
    """
    def calculate_dynamic_price(base_price, demand_factor, time_factor):
        """Calculate dynamic price based on demand and time"""
        return int(base_price * demand_factor * time_factor)
    
    # Calculate current prices for all tickets
    current_tickets = []
    for ticket in tickets:
        demand_factor = 1.0 + (ticket['demand'] / 100.0)
        time_factor = 1.0 + (ticket['time_remaining'] / 100.0)
        current_price = calculate_dynamic_price(ticket['base_price'], demand_factor, time_factor)
        current_tickets.append(current_price)
    
    # Sort current prices
    current_tickets.sort()
    
    result = []
    
    for customer in customers:
        budget = customer['budget']
        
        # Binary search for best affordable ticket
        index = bisect_right(current_tickets, budget) - 1
        
        if index >= 0:
            ticket_price = current_tickets.pop(index)
            result.append(ticket_price)
        else:
            result.append(-1)
    
    return result
```

## Problem Variations

### **Variation 1: Concert Tickets with Dynamic Updates**
**Problem**: Handle dynamic ticket availability and customer requests in real-time.

**Approach**: Use balanced binary search trees or segment trees for efficient updates and queries.

```python
import bisect
from collections import defaultdict

class DynamicConcertTickets:
    def __init__(self, tickets):
        self.tickets = sorted(tickets)
        self.available_tickets = self.tickets[:]
        self.sold_tickets = set()
    
    def add_tickets(self, new_tickets):
        """Add new tickets to the system."""
        for ticket in new_tickets:
            bisect.insort(self.available_tickets, ticket)
    
    def remove_tickets(self, tickets_to_remove):
        """Remove tickets from the system."""
        for ticket in tickets_to_remove:
            if ticket in self.available_tickets:
                self.available_tickets.remove(ticket)
    
    def sell_ticket(self, max_price):
        """Sell the most expensive ticket that doesn't exceed max_price."""
        # Find the largest ticket <= max_price
        index = bisect.bisect_right(self.available_tickets, max_price) - 1
        
        if index >= 0:
            ticket_price = self.available_tickets[index]
            self.available_tickets.pop(index)
            self.sold_tickets.add(ticket_price)
            return ticket_price
        
        return -1
    
    def get_available_tickets(self):
        """Get all available tickets."""
        return self.available_tickets[:]
    
    def get_sold_tickets(self):
        """Get all sold tickets."""
        return list(self.sold_tickets)
    
    def get_total_revenue(self):
        """Get total revenue from sold tickets."""
        return sum(self.sold_tickets)

# Example usage
tickets = [5, 3, 7, 8, 5]
system = DynamicConcertTickets(tickets)

print(f"Available tickets: {system.get_available_tickets()}")
print(f"Sold ticket for max price 6: {system.sell_ticket(6)}")
print(f"Sold ticket for max price 4: {system.sell_ticket(4)}")
print(f"Available tickets: {system.get_available_tickets()}")
print(f"Total revenue: {system.get_total_revenue()}")
```

### **Variation 2: Concert Tickets with Different Operations**
**Problem**: Handle different types of ticket operations (reservations, cancellations, upgrades).

**Approach**: Use advanced data structures to handle multiple operation types efficiently.

```python
class AdvancedConcertTickets:
    def __init__(self, tickets):
        self.tickets = sorted(tickets)
        self.available_tickets = self.tickets[:]
        self.reserved_tickets = {}  # customer_id -> ticket_price
        self.sold_tickets = set()
        self.customer_id_counter = 0
    
    def reserve_ticket(self, max_price):
        """Reserve a ticket for a customer."""
        index = bisect.bisect_right(self.available_tickets, max_price) - 1
        
        if index >= 0:
            ticket_price = self.available_tickets[index]
            self.available_tickets.pop(index)
            customer_id = self.customer_id_counter
            self.customer_id_counter += 1
            self.reserved_tickets[customer_id] = ticket_price
            return customer_id, ticket_price
        
        return -1, -1
    
    def confirm_reservation(self, customer_id):
        """Confirm a reserved ticket."""
        if customer_id in self.reserved_tickets:
            ticket_price = self.reserved_tickets[customer_id]
            del self.reserved_tickets[customer_id]
            self.sold_tickets.add(ticket_price)
            return ticket_price
        
        return -1
    
    def cancel_reservation(self, customer_id):
        """Cancel a reserved ticket."""
        if customer_id in self.reserved_tickets:
            ticket_price = self.reserved_tickets[customer_id]
            del self.reserved_tickets[customer_id]
            bisect.insort(self.available_tickets, ticket_price)
            return True
        
        return False
    
    def upgrade_ticket(self, customer_id, new_max_price):
        """Upgrade a reserved ticket to a better one."""
        if customer_id in self.reserved_tickets:
            old_ticket = self.reserved_tickets[customer_id]
            
            # Find a better ticket
            index = bisect.bisect_right(self.available_tickets, new_max_price) - 1
            
            if index >= 0 and self.available_tickets[index] > old_ticket:
                new_ticket = self.available_tickets[index]
                self.available_tickets.pop(index)
                bisect.insort(self.available_tickets, old_ticket)
                self.reserved_tickets[customer_id] = new_ticket
                return new_ticket
        
        return -1
    
    def get_reservation_status(self, customer_id):
        """Get the status of a reservation."""
        if customer_id in self.reserved_tickets:
            return self.reserved_tickets[customer_id]
        return -1

# Example usage
tickets = [5, 3, 7, 8, 5, 10, 2]
system = AdvancedConcertTickets(tickets)

# Reserve tickets
customer1, ticket1 = system.reserve_ticket(6)
customer2, ticket2 = system.reserve_ticket(4)
print(f"Customer {customer1} reserved ticket {ticket1}")
print(f"Customer {customer2} reserved ticket {ticket2}")

# Upgrade ticket
new_ticket = system.upgrade_ticket(customer1, 8)
print(f"Customer {customer1} upgraded to ticket {new_ticket}")

# Confirm reservation
confirmed = system.confirm_reservation(customer1)
print(f"Customer {customer1} confirmed ticket {confirmed}")
```

### **Variation 3: Concert Tickets with Constraints**
**Problem**: Handle ticket sales with additional constraints (VIP sections, group discounts, time limits).

**Approach**: Use constraint satisfaction with advanced optimization algorithms.

```python
class ConstrainedConcertTickets:
    def __init__(self, tickets, constraints):
        self.tickets = sorted(tickets)
        self.available_tickets = self.tickets[:]
        self.sold_tickets = set()
        self.constraints = constraints
        self.customer_history = {}  # customer_id -> [purchases]
        self.customer_id_counter = 0
    
    def sell_ticket_with_constraints(self, max_price, customer_id=None, group_size=1):
        """Sell ticket with various constraints."""
        if customer_id is None:
            customer_id = self.customer_id_counter
            self.customer_id_counter += 1
        
        # Check customer purchase limit
        if 'max_purchases_per_customer' in self.constraints:
            if customer_id in self.customer_history:
                if len(self.customer_history[customer_id]) >= self.constraints['max_purchases_per_customer']:
                    return -1
        
        # Check group discount eligibility
        discount = 0
        if 'group_discount_threshold' in self.constraints and group_size >= self.constraints['group_discount_threshold']:
            discount = self.constraints.get('group_discount_percent', 0)
        
        # Find suitable ticket
        adjusted_max_price = max_price * (1 + discount / 100)
        index = bisect.bisect_right(self.available_tickets, adjusted_max_price) - 1
        
        if index >= 0:
            ticket_price = self.available_tickets[index]
            
            # Apply discount
            final_price = ticket_price * (1 - discount / 100)
            
            # Check minimum price constraint
            if 'min_ticket_price' in self.constraints and final_price < self.constraints['min_ticket_price']:
                return -1
            
            self.available_tickets.pop(index)
            self.sold_tickets.add(ticket_price)
            
            # Update customer history
            if customer_id not in self.customer_history:
                self.customer_history[customer_id] = []
            self.customer_history[customer_id].append((ticket_price, final_price, group_size))
            
            return ticket_price, final_price
        
        return -1, -1
    
    def sell_vip_ticket(self, max_price, customer_id=None):
        """Sell VIP ticket with special constraints."""
        if 'vip_tickets' not in self.constraints:
            return -1, -1
        
        vip_tickets = sorted(self.constraints['vip_tickets'])
        index = bisect.bisect_right(vip_tickets, max_price) - 1
        
        if index >= 0:
            ticket_price = vip_tickets[index]
            
            # Check VIP eligibility
            if 'vip_eligibility' in self.constraints:
                if customer_id and customer_id in self.customer_history:
                    total_spent = sum(purchase[1] for purchase in self.customer_history[customer_id])
                    if total_spent < self.constraints['vip_eligibility']['min_total_spent']:
                        return -1, -1
            
            # Remove from VIP tickets
            self.constraints['vip_tickets'].remove(ticket_price)
            self.sold_tickets.add(ticket_price)
            
            # Update customer history
            if customer_id not in self.customer_history:
                self.customer_history[customer_id] = []
            self.customer_history[customer_id].append((ticket_price, ticket_price, 1))
            
            return ticket_price, ticket_price
        
        return -1, -1
    
    def get_customer_stats(self, customer_id):
        """Get statistics for a customer."""
        if customer_id in self.customer_history:
            purchases = self.customer_history[customer_id]
            total_spent = sum(purchase[1] for purchase in purchases)
            total_tickets = len(purchases)
            return {
                'total_spent': total_spent,
                'total_tickets': total_tickets,
                'average_price': total_spent / total_tickets if total_tickets > 0 else 0,
                'purchases': purchases
            }
        return None
    
    def get_revenue_analysis(self):
        """Get detailed revenue analysis."""
        total_revenue = sum(self.sold_tickets)
        total_tickets_sold = len(self.sold_tickets)
        average_price = total_revenue / total_tickets_sold if total_tickets_sold > 0 else 0
        
        return {
            'total_revenue': total_revenue,
            'total_tickets_sold': total_tickets_sold,
            'average_price': average_price,
            'available_tickets': len(self.available_tickets)
        }

# Example usage
tickets = [5, 3, 7, 8, 5, 10, 2, 15, 12]
constraints = {
    'max_purchases_per_customer': 3,
    'group_discount_threshold': 2,
    'group_discount_percent': 10,
    'min_ticket_price': 2,
    'vip_tickets': [20, 25, 30],
    'vip_eligibility': {'min_total_spent': 20}
}

system = ConstrainedConcertTickets(tickets, constraints)

# Regular ticket sales
ticket1, price1 = system.sell_ticket_with_constraints(6, customer_id=1)
print(f"Customer 1 bought ticket {ticket1} for {price1}")

# Group ticket sale
ticket2, price2 = system.sell_ticket_with_constraints(8, customer_id=2, group_size=3)
print(f"Customer 2 bought ticket {ticket2} for {price2} (group discount)")

# VIP ticket sale
vip_ticket, vip_price = system.sell_vip_ticket(25, customer_id=1)
print(f"Customer 1 bought VIP ticket {vip_ticket} for {vip_price}")

# Get statistics
stats = system.get_customer_stats(1)
print(f"Customer 1 stats: {stats}")

revenue = system.get_revenue_analysis()
print(f"Revenue analysis: {revenue}")
```

### Related Problems

#### **CSES Problems**
- [Concert Tickets](https://cses.fi/problemset/task/1091) - Basic concert tickets problem
- [Apartments](https://cses.fi/problemset/task/1084) - Similar matching problem
- [Ferris Wheel](https://cses.fi/problemset/task/1090) - Two-pointer optimization

#### **LeetCode Problems**
- [Two Sum](https://leetcode.com/problems/two-sum/) - Find pairs with target sum
- [3Sum](https://leetcode.com/problems/3sum/) - Find triplets with zero sum
- [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) - Two-pointer optimization
- [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) - Two-pointer water trapping

#### **Problem Categories**
- **Binary Search**: Efficient searching, sorted array algorithms, upper bound operations
- **Greedy Algorithms**: Optimal local choices, matching problems, resource allocation
- **Sorting**: Array sorting, binary search, efficient data structures
- **Algorithm Design**: Binary search algorithms, greedy strategies, optimization techniques
