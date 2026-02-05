# Tree Summing

## Problem Information
- **Source:** UVa
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

## Problem Statement

LISP was one of the earliest high-level programming languages. Lists, which are the fundamental data structures in LISP, can easily be adapted to represent other important data structures such as trees.

Given a binary tree of integers, you are to write a program that determines whether there exists a root-to-leaf path whose nodes sum to a specified integer.

Binary trees are represented in the input file as LISP S-expressions having the following form:
- empty tree ::= ()
- tree ::= empty tree | (integer tree tree)

Example: `(5 (4 (11 (7 () ()) (2 () ())) ()) (8 (13 () ()) (4 () (1 () ()))))`

Note that with this formulation all leaves of a tree are of the form `(integer () ())`

## Input Format
- The input consists of a sequence of test cases in the form of integer/tree pairs.
- Each test case consists of an integer followed by one or more spaces followed by a binary tree formatted as an S-expression.
- Expressions may be spread over several lines and may contain spaces.
- Input is terminated by end-of-file.

## Output Format
For each pair I, T (I represents the integer, T represents the tree), output "yes" if there is a root-to-leaf path in T whose sum is I and "no" if there is no such path.

## Solution

### Approach
Parse the LISP S-expression and use recursion/stack to track the current path sum. When we encounter a leaf node (integer () ()), check if the sum equals the target.

### Python Solution

```python
import sys

def solve():
 data = sys.stdin.read()
 idx = 0
 n = len(data)

 def skip_whitespace():
  nonlocal idx
  while idx < n and data[idx] in ' \t\n\r':
   idx += 1

 def parse_int():
  nonlocal idx
  skip_whitespace()
  negative = False
  if idx < n and data[idx] == '-':
   negative = True
   idx += 1
  num = 0
  while idx < n and data[idx].isdigit():
   num = num * 10 + int(data[idx])
   idx += 1
  return -num if negative else num

 def parse_tree(target, current_sum):
  """Returns True if there's a root-to-leaf path with sum = target"""
  nonlocal idx
  skip_whitespace()

  if idx >= n or data[idx] != '(':
   return False

  idx += 1  # Skip '('
  skip_whitespace()

  # Check for empty tree
  if data[idx] == ')':
   idx += 1
   return None  # Empty tree marker

  # Parse integer
  value = parse_int()
  current_sum += value

  # Parse left subtree
  left_result = parse_tree(target, current_sum)

  # Parse right subtree
  right_result = parse_tree(target, current_sum)

  skip_whitespace()
  idx += 1  # Skip ')'

  # If both children are empty (leaf node)
  if left_result is None and right_result is None:
   return current_sum == target

  # If one child is empty, check the other
  if left_result is None:
   return right_result
  if right_result is None:
   return left_result

  # Both children exist
  return left_result or right_result

 while idx < n:
  skip_whitespace()
  if idx >= n:
   break

  # Check if we have an integer (target)
  if data[idx].isdigit() or data[idx] == '-':
   target = parse_int()
   skip_whitespace()

   if idx >= n or data[idx] != '(':
    break

   # Check for empty tree
   result = parse_tree(target, 0)

   if result is None:
    print("no")  # Empty tree
   else:
    print("yes" if result else "no")
  else:
   idx += 1

if __name__ == "__main__":
 solve()
```

### Alternative Solution with Stack

```python
import sys
import re

def solve():
 data = sys.stdin.read()

 # Extract all tokens: integers and parentheses
 tokens = re.findall(r'-?\d+|\(|\)', data)

 i = 0
 while i < len(tokens):
  # Read target sum
  target = int(tokens[i])
  i += 1

  stack = []  # Stack of (value, null_count)
  current_sum = 0
  found = False

  while i < len(tokens):
   token = tokens[i]
   i += 1

   if token == '(':
    if i < len(tokens) and tokens[i] not in '()':
     # This is a node with a value
     value = int(tokens[i])
     i += 1
     stack.append((value, 0))
     current_sum += value
    else:
     # Empty tree marker
     if stack:
      val, null_count = stack[-1]
      stack[-1] = (val, null_count + 1)

   elif token == ')':
    if not stack:
     break  # End of tree

    val, null_count = stack[-1]

    if null_count >= 2:
     # This is a leaf node
     if current_sum == target:
      found = True

     # Pop this node
     stack.pop()
     current_sum -= val

     # Update parent's null count
     if stack:
      parent_val, parent_null = stack[-1]
      stack[-1] = (parent_val, parent_null + 1)
    else:
     # Not enough children processed yet
     pass

  print("yes" if found else "no")

if __name__ == "__main__":
 solve()
```

### Complexity Analysis
- **Time Complexity:** O(N) where N is the length of the input string
- **Space Complexity:** O(H) where H is the height of the tree (for recursion stack)

### Key Insight
The main challenge is parsing the LISP S-expression correctly. A leaf node is identified when both its children are empty trees `()`. Only at leaf nodes do we check if the accumulated sum equals the target.
