---
layout: simple
title: "Trie"
permalink: /problem_soulutions/Blue/Session 17 - Trie/
---

# Trie

This session covers Trie (prefix tree) data structure for efficient string storage, prefix matching, and autocomplete operations.

## Problems

### Bank Password Security

#### Problem Information
- **Source:** CodeChef
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

A bank's password system is vulnerable if any password is a prefix of another. Given n passwords, determine if the system is vulnerable or not.

#### Input Format
- First line: n (number of passwords)
- Next n lines: one password per line

#### Output Format
- "vulnerable" if any password is a prefix of another
- "non vulnerable" otherwise

#### Example
```
Input:
3
abc
abcd
xyz

Output:
vulnerable
```

#### Solution

##### Approach
Build a Trie (prefix tree) with all passwords. While inserting, check if current password is prefix of existing one or if an existing password is prefix of current one.

##### Python Solution

```python
import sys


class InputTokenizer:
  def __init__(self):
    self._tokens = sys.stdin.read().split()[::-1]

  def has_next(self):
    return bool(self._tokens)

  def next(self):
    return self._tokens.pop()


inp = InputTokenizer()


class TrieNode:
  def __init__(self):
    self.is_word = False
    self.child = {}


def add_word(root, s):
  node = root
  for ch in s:
    if ch not in node.child:
      node.child[ch] = TrieNode()
    node = node.child[ch]
    if node.is_word:  # Existing word is prefix of new
      return False
  if node.child:  # New word is prefix of existing
    return False
  node.is_word = True
  return True


def solution():
  root = TrieNode()
  n = int(inp.next())

  for _ in range(n):
    if not add_word(root, inp.next()):
      print('vulnerable')
      return

  print('non vulnerable')


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n * L) where L is average password length
- **Space Complexity:** O(n * L) for Trie storage

---

### Old Berland Language

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

#### Problem Statement

Construct n binary strings of given lengths such that no string is a prefix of another. This is essentially building a prefix-free code (like Huffman codes).

#### Input Format
- First line: n (number of words needed)
- Next n lines: length of each word

#### Output Format
- "YES" followed by n binary strings, or "NO" if impossible

#### Example
```
Input:
3
1
2
2

Output:
YES
0
10
11
```

#### Solution

##### Approach
Sort words by required length. Use DFS to traverse a binary tree, assigning binary strings at required depths. Each leaf (assigned string) blocks its entire subtree. Track which depths are needed and assign strings greedily.

##### Python Solution

```python
import sys


class InputTokenizer:
  def __init__(self):
    self._tokens = sys.stdin.read().split()[::-1]

  def next(self):
    return self._tokens.pop()


inp = InputTokenizer()


def dfs(n, arr):
  """DFS to assign binary strings at required depths."""
  word = [''] * n
  stack = [('', 0)]  # (current_string, depth)
  curr = 0

  while stack and curr < n:
    s, depth = stack.pop()

    if arr[curr][0] == depth:
      word[arr[curr][1]] = s
      curr += 1
      continue

    # Add children: '1' first so '0' is popped first (lexicographic order)
    stack.append((s + '1', depth + 1))
    stack.append((s + '0', depth + 1))

  return curr, word


def solution():
  n = int(inp.next())
  # Store (depth, original_index) pairs
  arr = [(int(inp.next()), i) for i in range(n)]
  arr.sort()  # Sort by depth

  curr, word = dfs(n, arr)

  if curr < n:
    print('NO')
  else:
    print('YES')
    print(*word, sep='\n')


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(2^max_depth) in worst case, but bounded by n
- **Space Complexity:** O(n) for storing results

---

### Search Engine

#### Problem Information
- **Source:** Hackerearth
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Build a search engine that stores strings with associated weights. For each query prefix, return the maximum weight among all strings that start with that prefix.

#### Input Format
- First line: n (number of strings), q (number of queries)
- Next n lines: string and its weight
- Next q lines: query prefix

#### Output Format
For each query: maximum weight of strings with that prefix, or -1 if none.

#### Example
```
Input:
5 3
apple 10
application 15
app 5
banana 20
band 12
app
ban
cat

Output:
15
20
-1
```

#### Solution

##### Approach
Build a Trie where each node stores the maximum weight seen in its subtree. When inserting, propagate max weight up through the path. Query by traversing to the prefix node and returning its maxWeight.

##### Python Solution

```python
class TrieNode:
  def __init__(self):
    self.max_weight = 0
    self.child = {}


def add_word(root, s, weight):
  node = root
  for ch in s:
    if ch not in node.child:
      node.child[ch] = TrieNode()
    node = node.child[ch]
    node.max_weight = max(node.max_weight, weight)


def find_max_weight(root, prefix):
  node = root
  for ch in prefix:
    if ch not in node.child:
      return -1
    node = node.child[ch]
  return node.max_weight


def solution():
  n, q = map(int, input().split())
  root = TrieNode()

  for _ in range(n):
    s, weight = input().strip().split()
    add_word(root, s, int(weight))

  for _ in range(q):
    print(find_max_weight(root, input().strip()))


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(L) for both insert and query where L is string length
- **Space Complexity:** O(n * L) for Trie storage

---

### No Prefix Set

#### Problem Information
- **Source:** Hackerrank
- **Difficulty:** Secret
- **Time Limit:** 4000ms
- **Memory Limit:** 512MB

#### Problem Statement

Given a set of strings, determine if it forms a "GOOD SET" where no string is a prefix of another. If a prefix conflict exists, output "BAD SET" and the offending string.

#### Input Format
- First line: n (number of strings)
- Next n lines: one string per line

#### Output Format
- "GOOD SET" if no string is a prefix of another
- "BAD SET" followed by the first string causing the conflict

#### Example
```
Input:
4
aab
aac
aacghgh
aabghgh

Output:
BAD SET
aacghgh
```

#### Solution

##### Approach
Build a Trie incrementally. For each new string, check:
1. If we pass through a word-end node (existing string is prefix of new)
2. If current string ends at non-leaf node (new string is prefix of existing)

##### Python Solution

```python
import sys


class InputTokenizer:
  def __init__(self):
    self._tokens = sys.stdin.read().split()[::-1]

  def next(self):
    return self._tokens.pop()


inp = InputTokenizer()


class TrieNode:
  def __init__(self):
    self.is_word = False
    self.child = {}


def add_word(root, s):
  """Returns (success, offending_string)."""
  node = root
  for ch in s:
    if ch not in node.child:
      node.child[ch] = TrieNode()
    node = node.child[ch]
    if node.is_word:
      return False, s

  if node.child:
    return False, s
  node.is_word = True
  return True, None


def solution():
  root = TrieNode()
  n = int(inp.next())

  for _ in range(n):
    s = inp.next()
    success, bad_string = add_word(root, s)
    if not success:
      print('BAD SET')
      print(bad_string)
      return

  print('GOOD SET')


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n * L) where L is average string length
- **Space Complexity:** O(n * L)

---

### Contacts

#### Problem Information
- **Source:** Hackerrank
- **Difficulty:** Secret
- **Time Limit:** 4000ms
- **Memory Limit:** 512MB

#### Problem Statement

Implement a contact list with two operations:
- add <name>: Add a contact name to the list
- find <partial>: Count contacts starting with the given partial name

#### Input Format
- First line: n (number of operations)
- Next n lines: operation and argument

#### Output Format
For each "find" operation: number of contacts with matching prefix.

#### Example
```
Input:
4
add hack
add hackerrank
find hac
find hak

Output:
2
0
```

#### Solution

##### Approach
Use a Trie where each node maintains a count of words passing through it. When adding, increment count at each node along the path. When finding, traverse to prefix node and return its count.

##### Python Solution

```python
import sys


class InputTokenizer:
  def __init__(self):
    self._tokens = sys.stdin.read().split()[::-1]

  def next(self):
    return self._tokens.pop()


inp = InputTokenizer()


class TrieNode:
  def __init__(self):
    self.count = 0  # Words passing through this node
    self.child = {}


def add_word(root, s):
  node = root
  for ch in s:
    if ch not in node.child:
      node.child[ch] = TrieNode()
    node = node.child[ch]
    node.count += 1


def find_prefix_count(root, prefix):
  node = root
  for ch in prefix:
    if ch not in node.child:
      return 0
    node = node.child[ch]
  return node.count


def solution():
  root = TrieNode()
  n = int(inp.next())

  for _ in range(n):
    op, word = inp.next(), inp.next()
    if op == 'add':
      add_word(root, word)
    elif op == 'find':
      print(find_prefix_count(root, word))


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(L) for both add and find operations
- **Space Complexity:** O(n * L)

---

### Consistency Checker

#### Problem Information
- **Source:** LightOJ
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 32MB

#### Problem Statement

A phone directory is consistent if no phone number is a prefix of another. Given a list of phone numbers, check if the directory is consistent.

#### Input Format
- First line: T (test cases)
- For each test case:
  - n (number of phone numbers)
  - n phone numbers (digits only)

#### Output Format
For each test case: "Case X: YES" if consistent, "Case X: NO" otherwise.

#### Example
```
Input:
2
3
911
97625999
91125426
3
113
12340
123

Output:
Case 1: NO
Case 2: YES
```

#### Solution

##### Approach
Build a Trie with phone numbers. Check for prefix conflicts during insertion:
- If a complete number exists along the path (prefix of current)
- If current number ends at a non-leaf (current is prefix of existing)

##### Python Solution

```python
class TrieNode:
  def __init__(self):
    self.is_word = False
    self.child = {}


def add_word(root, s):
  node = root
  for ch in s:
    if ch not in node.child:
      node.child[ch] = TrieNode()
    node = node.child[ch]
    if node.is_word:
      return False
  if node.child:
    return False
  node.is_word = True
  return True


def solution():
  T = int(input())
  for t in range(T):
    root = TrieNode()
    n = int(input())
    consistent = True

    for _ in range(n):
      if not add_word(root, input().strip()):
        print(f'Case {t + 1}: NO')
        consistent = False
        break

    if consistent:
      print(f'Case {t + 1}: YES')


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n * L) where L is average phone number length
- **Space Complexity:** O(n * L)

---

### DNA Prefix

#### Problem Information
- **Source:** LightOJ
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 32MB

#### Problem Statement

Given a set of DNA strings, find the maximum "prefix score". The prefix score of a set is defined as (length of common prefix) * (number of strings). Find the maximum score achievable by any subset sharing a common prefix.

#### Input Format
- First line: T (test cases)
- For each test case:
  - n (number of DNA strings)
  - n DNA strings (containing A, C, G, T)

#### Output Format
For each test case: "Case X: max_score"

#### Example
```
Input:
1
4
ACGT
ACGTG
ACGA
ACG

Output:
Case 1: 12
```

#### Solution

##### Approach
Build a Trie with DNA strings. Each node tracks cumulative "weight" = sum of depths of strings passing through. Maximum weight at any node represents the best prefix score.

##### Python Solution

```python
class TrieNode:
  def __init__(self):
    self.weight = 0
    self.child = {}


def add_word(root, s):
  """Add word and return max prefix score encountered."""
  node = root
  max_weight = 0
  for i, ch in enumerate(s, 1):
    if ch not in node.child:
      node.child[ch] = TrieNode()
    node = node.child[ch]
    node.weight += i
    max_weight = max(max_weight, node.weight)
  return max_weight


def solution():
  T = int(input())
  for t in range(T):
    n = int(input())
    root = TrieNode()
    max_weight = max(add_word(root, input()) for _ in range(n))
    print(f'Case {t + 1}: {max_weight}')


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n * L) where L is average string length
- **Space Complexity:** O(n * L)

---

### Product Suggestions

#### Problem Information
- **Source:** Custom (Amazon/LeetCode style)
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given a product repository and a customer search query, suggest up to 3 products for each prefix of the query (starting from 2 characters). Products should be suggested in lexicographical order.

#### Input Format
- numProducts: number of products in repository
- repository: list of product names
- customerQuery: search string

#### Output Format
List of lists: for each prefix of query (length 2 onwards), up to 3 lexicographically smallest matching products.

#### Example
```
Input:
numProducts = 5
repository = ['code', 'codePhone', 'coddle', 'coddles', 'codes']
customerQuery = 'coddle'

Output:
[['code', 'codePhone', 'coddle'], ['code', 'codePhone', 'coddle'], ['coddle', 'coddles'], ['coddle', 'coddles'], ['coddle', 'coddles']]
```

#### Solution

##### Approach
Build a Trie from all product names. For each query prefix, find the Trie node. Extract up to 3 words from that subtree in lexicographical order. Uses DFS with sorted child keys for ordered traversal.

##### Python Solution

```python
class TrieNode:
  def __init__(self):
    self.child = {}
    self.is_word = False


def add_word(root, s):
  node = root
  for ch in s:
    if ch not in node.child:
      node.child[ch] = TrieNode()
    node = node.child[ch]
  node.is_word = True


def find_node(root, prefix):
  node = root
  for ch in prefix:
    if ch not in node.child:
      return None
    node = node.child[ch]
  return node


def extract_words(node, limit=3):
  """Extract up to `limit` words from subtree in lexicographic order."""
  result = []

  def dfs(curr, suffix):
    if len(result) >= limit:
      return
    if curr.is_word:
      result.append(suffix)
    for ch in sorted(curr.child):
      if len(result) >= limit:
        return
      dfs(curr.child[ch], suffix + ch)

  dfs(node, '')
  return result


def three_product_suggestions(repository, query):
  root = TrieNode()
  for product in repository:
    add_word(root, product)

  results = []
  for i in range(2, len(query) + 1):
    prefix = query[:i]
    node = find_node(root, prefix)
    if not node:
      break
    results.append([prefix + suffix for suffix in extract_words(node)])

  return results


# Example usage
repository = ['code', 'codePhone', 'coddle', 'coddles', 'codes']
query = 'coddle'
print(three_product_suggestions(repository, query))
```

##### Complexity Analysis
- **Time Complexity:** O(n * L) for building Trie, O(Q * 3) for queries
- **Space Complexity:** O(n * L)

---

### Diccionario Portunol

#### Problem Information
- **Source:** ICPC Archive
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

Create a "Portunol" dictionary by combining Portuguese and Spanish words. A Portunol word is formed by taking a prefix of a Portuguese word and appending a suffix of a Spanish word. Count the number of distinct Portunol words that can be formed.

#### Input Format
- Multiple test cases until P=S=0
- P (Portuguese words), S (Spanish words)
- P Portuguese words
- S Spanish words

#### Output Format
For each test case: number of distinct Portunol words.

#### Example
```
Input:
2 2
abc
de
fg
hi
0 0

Output:
8
```

#### Solution

##### Approach
Use a Trie to store and count unique combined words. For each Portuguese word prefix (length 1 to full length), combine with each Spanish word suffix (all possible suffixes). Add to Trie and count only new unique words.

##### Python Solution

```python
import sys


class InputTokenizer:
  def __init__(self):
    self._tokens = sys.stdin.read().split()[::-1]

  def next(self):
    return self._tokens.pop()


inp = InputTokenizer()


class TrieNode:
  def __init__(self):
    self.is_word = False
    self.child = {}


def add_word(root, s):
  """Returns True if word is new, False if already exists."""
  node = root
  for ch in s:
    if ch not in node.child:
      node.child[ch] = TrieNode()
    node = node.child[ch]
  if node.is_word:
    return False
  node.is_word = True
  return True


def solution():
  while True:
    P, S = int(inp.next()), int(inp.next())
    if P == 0 and S == 0:
      break

    p_words = [inp.next() for _ in range(P)]
    s_words = [inp.next() for _ in range(S)]

    root = TrieNode()
    total = 0

    for p_word in p_words:
      for k in range(1, len(p_word) + 1):
        prefix = p_word[:k]
        for s_word in s_words:
          for l in range(len(s_word)):
            if add_word(root, prefix + s_word[l:]):
              total += 1

    print(total)


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(P * L_p * S * L_s) where L_p and L_s are average word lengths
- **Space Complexity:** O(total unique words * average length)
