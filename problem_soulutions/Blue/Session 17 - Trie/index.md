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
Password "abc" is a prefix of "abcd", making the system vulnerable.

#### Solution

##### Approach
Build a Trie (prefix tree) with all passwords. While inserting, check if current password is prefix of existing one or if an existing password is prefix of current one.

##### Python Solution

```python
import sys


class input_tokenizer:
  __tokens = None

  def has_next(self):
    return self.__tokens != [] and self.__tokens != None

  def next(self):
    token = self.__tokens[-1]
    self.__tokens.pop()
    return token

  def __init__(self):
    self.__tokens = sys.stdin.read().split()[::-1]


inp = input_tokenizer()


class Node:
  def __init__(self):
    self.countWord = 0
    self.child = dict()


def add_word(root, s):
  tmp = root
  for ch in s:
    if ch not in tmp.child:
      tmp.child[ch] = Node()
    tmp = tmp.child[ch]
    if tmp.countWord > 0:
      return False
  if len(tmp.child) > 0:
    return False
  tmp.countWord += 1
  return True


def solution():
  root = Node()
  n = int(inp.next())
  duplicated = False
  for i in range(n):
    s = inp.next()
    if not add_word(root, s):
      print('vulnerable')
      duplicated = True
      break
  if not duplicated:
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
Three binary strings of lengths 1, 2, 2 with no prefix conflicts: "0", "10", "11".

#### Solution

##### Approach
Sort words by required length. Use DFS to traverse a binary tree, assigning binary strings at required depths. Each leaf (assigned string) blocks its entire subtree. Track which depths are needed and assign strings greedily.

##### Python Solution

```python
import sys


class input_tokenizer:
  __tokens = None

  def has_next(self):
    return self.__tokens != [] and self.__tokens != None

  def next(self):
    token = self.__tokens[-1]
    self.__tokens.pop()
    return token

  def __init__(self):
    self.__tokens = sys.stdin.read().split()[::-1]


inp = input_tokenizer()


class Node:
  def __init__(self, index, depth):
    self.index = index
    self.depth = depth

  def __lt__(self, other):
    return self.depth < other.depth


def dfs(s, depth, n, curr, word, arr):
  stack = [[s, depth]]

  while True:
    if len(stack) == 0:
      break
    s, depth = stack.pop()
    if curr >= n:
      return curr, word

    if arr[curr].depth == depth:
      word[arr[curr].index] = s
      curr += 1
      continue

    next_s = s + '0'
    stack.append([next_s, depth + 1])

    next_s = s + '1'
    stack.append([next_s, depth + 1])

  return curr, word


def solution():
  try:
    n = int(inp.next())
    arr = []

    for i in range(n):
      word_len = int(inp.next())
      arr.append(Node(i, word_len))

    arr.sort()

    word = ['' for i in range(n)]
    curr = 0
    results = dfs('', 0, n, curr, word, arr)

    word = results[1]
    curr = results[0]

    if curr < n:
      print('NO')
    else:
      print('YES')
      print(*word, sep='\n')
  except Exception as ex:
    print(ex)


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
"app" matches "apple"(10), "application"(15), "app"(5) - max is 15. "ban" matches "banana"(20), "band"(12) - max is 20. "cat" has no matches.

#### Solution

##### Approach
Build a Trie where each node stores the maximum weight seen in its subtree. When inserting, propagate max weight up through the path. Query by traversing to the prefix node and returning its maxWeight.

##### Python Solution

```python
class Node:
  def __init__(self):
    self.maxWeight = 0
    self.child = dict()


def add_word(root, s, weight):
  tmp = root
  for ch in s:
    if ch not in tmp.child:
      tmp.child[ch] = Node()
    tmp = tmp.child[ch]
    if tmp.maxWeight < weight:
      tmp.maxWeight = weight


def find_word_max_weight(root, s):
  tmp = root
  for ch in s:
    if ch not in tmp.child:
      return -1
    tmp = tmp.child[ch]
  return tmp.maxWeight


def solution():
  n, q = map(int, input().split())
  root = Node()
  for i in range(n):
    s, weight = map(str, input().strip().split())
    weight = int(weight)
    add_word(root, s, weight)

  for i in range(q):
    word = input().strip()
    print(find_word_max_weight(root, word))


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
"aac" is a prefix of "aacghgh", so "aacghgh" causes the conflict.

#### Solution

##### Approach
Build a Trie incrementally. For each new string, check:
1. If we pass through a word-end node (existing string is prefix of new)
2. If current string ends at non-leaf node (new string is prefix of existing)

##### Python Solution

```python
import sys


class input_tokenizer:
  __tokens = None

  def has_next(self):
    return self.__tokens != [] and self.__tokens != None

  def next(self):
    token = self.__tokens[-1]
    self.__tokens.pop()
    return token

  def __init__(self):
    self.__tokens = sys.stdin.read().split()[::-1]


inp = input_tokenizer()


class Node:
  def __init__(self):
    self.countWord = 0
    self.child = dict()


def add_word(root, s):
  tmp = root
  for ch in s:
    if ch not in tmp.child:
      tmp.child[ch] = Node()
    tmp = tmp.child[ch]
    if tmp.countWord > 0:
      return False, s

  if len(tmp.child) > 0:
    return False, s
  tmp.countWord += 1
  return 'GOOD SET'


def solution():
  root = Node()
  n = int(inp.next())
  duplicated = False
  for i in range(n):
    s = inp.next()
    result = add_word(root, s)
    if not result[0]:
      print('BAD SET')
      print(result[1])
      duplicated = True
      break
  if not duplicated:
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
After adding "hack" and "hackerrank", "hac" matches both (count 2). "hak" matches none (count 0).

#### Solution

##### Approach
Use a Trie where each node maintains a count of words passing through it. When adding, increment count at each node along the path. When finding, traverse to prefix node and return its count.

##### Python Solution

```python
import sys


class input_tokenizer:
  __tokens = None

  def has_next(self):
    return self.__tokens != [] and self.__tokens != None

  def next(self):
    token = self.__tokens[-1]
    self.__tokens.pop()
    return token

  def __init__(self):
    self.__tokens = sys.stdin.read().split()[::-1]


inp = input_tokenizer()


class Node:
  def __init__(self):
    self.countWord = 0
    self.child = dict()


def add_word(root, s):
  tmp = root
  for ch in s:
    if ch not in tmp.child:
      tmp.child[ch] = Node()
    tmp = tmp.child[ch]
    tmp.countWord += 1


def find_word(root, s):
  tmp = root
  for ch in s:
    if ch not in tmp.child:
      return 0
    tmp = tmp.child[ch]
  return tmp.countWord


def solution():
  root = Node()
  n = int(inp.next())
  for i in range(n):
    q = inp.next()
    word = inp.next()
    if q == 'add':
      add_word(root, word)
    if q == 'find':
      print(find_word(root, word))


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
Case 1: "911" is a prefix of "91125426". Case 2: No number is a prefix of another.

#### Solution

##### Approach
Build a Trie with phone numbers. Check for prefix conflicts during insertion:
- If a complete number exists along the path (prefix of current)
- If current number ends at a non-leaf (current is prefix of existing)

##### Python Solution

```python
class Node:
  def __init__(self):
    self.countWord = 0
    self.child = dict()


def add_word(root, s):
  tmp = root
  for ch in s:
    if ch not in tmp.child:
      tmp.child[ch] = Node()
    tmp = tmp.child[ch]
    if tmp.countWord > 0:
      return False
  if len(tmp.child) > 0:
    return False
  tmp.countWord += 1
  return True


def solution():
  T = int(input())
  for t in range(T):
    root = Node()
    n = int(input())
    duplicated = False
    for i in range(n):
      s = input().strip()
      if not add_word(root, s):
        print('Case {}: NO'.format(t + 1))
        duplicated = True
        break
    if not duplicated:
      print('Case {}: YES'.format(t + 1))


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
Prefix "ACG" is shared by all 4 strings. Score = length(3) * count(4) = 12. This is the maximum achievable.

#### Solution

##### Approach
Build a Trie with DNA strings. Each node tracks cumulative "weight" = sum of depths of strings passing through. Maximum weight at any node represents the best prefix score.

##### Python Solution

```python
class Node:
  def __init__(self):
    self.maxWeight = 0
    self.child = dict()


def add_word(root, s):
  tmp = root
  i = 1
  max_weight = 0
  for ch in s:
    if ch not in tmp.child:
      tmp.child[ch] = Node()
    tmp = tmp.child[ch]
    tmp.maxWeight += i
    i += 1
    if tmp.maxWeight > max_weight:
      max_weight = tmp.maxWeight
  return max_weight


def find_word_max_weight(root, s):
  tmp = root
  for ch in s:
    if ch not in tmp.child:
      return -1
    tmp = tmp.child[ch]
  return tmp.maxWeight


def solution():
  T = int(input())
  for t in range(T):
    n = int(input())
    root = Node()
    max_weight = 0
    for i in range(n):
      s = input()
      current_max_weight = add_word(root, s)
      if max_weight < current_max_weight:
        max_weight = current_max_weight

    print('Case {}: {}'.format(t + 1, max_weight))


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
For prefix "co": all 5 match, return first 3 alphabetically. For "codd": only coddle/coddles match.

#### Solution

##### Approach
Build a Trie from all product names. For each query prefix, find the Trie node. Extract up to 3 words from that subtree in lexicographical order. Uses DFS with sorted child keys for ordered traversal.

##### Python Solution

```python
class Node:
  def __init__(self):
    self.child = dict()
    self.word_count = 0


def add_word(root, s):
  tmp = root
  for ch in s:
    if ch not in tmp.child:
      tmp.child[ch] = Node()
    tmp = tmp.child[ch]
  tmp.word_count += 1


def find_word(root, s):
  tmp = root
  for ch in s:
    if ch not in tmp.child:
      return []
    tmp = tmp.child[ch]
  return tmp


def extract_words(found_node):
  result = []

  if found_node.child:
    if found_node.word_count > 0:
      result.append('')
      if len(result) >= 3:
        return result

    current_keys = sorted(list(found_node.child.keys()))
    for k in current_keys:
      for s in extract_words(found_node.child[k]):
        result.append(k + s)
        if len(result) >= 3:
          return result
  else:
    result.append('')
  return result


def threeProductSuggestions(numProducts, repository, customerQuery):
  root = Node()
  for i in range(numProducts):
    add_word(root, repository[i])

  results = []
  for i in range(2, len(customerQuery) + 1):
    current_query = customerQuery[:i]
    found_node = find_word(root, current_query)
    if not found_node:
      break

    result = extract_words(found_node)
    for k in range(len(result)):
      result[k] = current_query + result[k]

    results.append(result)

  return results


numProducts = 5
repository = ['code', 'codePhone', 'coddle', 'coddles', 'codes']
customerQuery = 'coddle'

print(threeProductSuggestions(numProducts, repository, customerQuery))
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
Portuguese prefixes: "a", "ab", "abc", "d", "de". Spanish suffixes for each. Combinations: a+fg, a+g, a+hi, a+i, ab+fg, ab+g, etc. Total unique = 8.

#### Solution

##### Approach
Use a Trie to store and count unique combined words. For each Portuguese word prefix (length 1 to full length), combine with each Spanish word suffix (all possible suffixes). Add to Trie and count only new unique words.

##### Python Solution

```python
import sys


class input_tokenizer:
  __tokens = None

  def has_next(self):
    return self.__tokens != [] and self.__tokens != None

  def next(self):
    token = self.__tokens[-1]
    self.__tokens.pop()
    return token

  def __init__(self):
    self.__tokens = sys.stdin.read().split()[::-1]


inp = input_tokenizer()


class Node:
  def __init__(self):
    self.countWord = 0
    self.child = dict()


def add_word(root, s):
  tmp = root
  for ch in s:
    if ch not in tmp.child:
      tmp.child[ch] = Node()
    tmp = tmp.child[ch]
  if tmp.countWord > 0:
    return False
  tmp.countWord += 1
  return True


def solution():
  while True:
    P = int(inp.next())
    S = int(inp.next())
    P_words = []
    S_words = []
    root = Node()
    if P == 0 and S == 0:
      break
    for i in range(P):
      P_words.append(inp.next())

    for i in range(S):
      S_words.append(inp.next())

    total = 0
    for i in range(P):
      p_len = len(P_words[i])
      for k in range(1, p_len + 1):
        for j in range(S):
          s_len = len(S_words[j])
          for l in range(s_len):
            new_word = P_words[i][:k] + S_words[j][l:s_len]
            if add_word(root, new_word):
              total += 1
    print(total)


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(P * L_p * S * L_s) where L_p and L_s are average word lengths
- **Space Complexity:** O(total unique words * average length)
