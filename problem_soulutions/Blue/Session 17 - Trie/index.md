---
layout: simple
title: "Session 17 - Trie"
permalink: /problem_soulutions/Blue/Session 17 - Trie/
---

# Session 17 - Trie

This session covers Trie (prefix tree) data structure for efficient string storage, prefix matching, and autocomplete operations.

## Problems

### BANKPASS (CodeChef)

```python
# Problem from CodeChef
# https://www.codechef.com/problems/BANKPASS
#
# Problem: Bank Password Security
#
# Description:
# A bank's password system is vulnerable if any password is a prefix of another.
# Given n passwords, determine if the system is vulnerable or not.
#
# Input:
# - First line: n (number of passwords)
# - Next n lines: one password per line
#
# Output:
# - "vulnerable" if any password is a prefix of another
# - "non vulnerable" otherwise
#
# Approach:
# - Build a Trie (prefix tree) with all passwords
# - While inserting, check if current password is prefix of existing one
#   or if an existing password is prefix of current one
# - Time complexity: O(n * L) where L is average password length

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

### 37C (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/contest/37/problem/C
#
# Problem: Old Berland Language
#
# Description:
# Construct n binary strings of given lengths such that no string is a
# prefix of another. This is essentially building a prefix-free code
# (like Huffman codes).
#
# Input:
# - First line: n (number of words needed)
# - Next n lines: length of each word
#
# Output:
# - "YES" followed by n binary strings, or "NO" if impossible
#
# Approach:
# - Sort words by required length
# - Use DFS to traverse a binary tree, assigning binary strings at required depths
# - Each leaf (assigned string) blocks its entire subtree
# - Track which depths are needed and assign strings greedily

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
        # curr, word = dfs(s, depth + 1, n, curr, word, arr)

        next_s = s + '1'
        stack.append([next_s, depth + 1])
        # curr, word = dfs(s, depth + 1, n, curr, word, arr)

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
        # import traceback
        # print(traceback.format_exc())
        print(ex)


solution()
```

### search_engine (Hackerearth)

```python
# Problem from Hackerearth
# https://www.hackerearth.com/practice/data-structures/advanced-data-structures/trie-keyword-tree/practice-problems/algorithm/search-engine/
#
# Problem: Search Engine
#
# Description:
# Build a search engine that stores strings with associated weights.
# For each query prefix, return the maximum weight among all strings
# that start with that prefix.
#
# Input:
# - First line: n (number of strings), q (number of queries)
# - Next n lines: string and its weight
# - Next q lines: query prefix
#
# Output:
# - For each query: maximum weight of strings with that prefix, or -1 if none
#
# Approach:
# - Build a Trie where each node stores the maximum weight seen in its subtree
# - When inserting, propagate max weight up through the path
# - Query by traversing to the prefix node and returning its maxWeight


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

### No_prefix_set (Hackerrank)

```python
# Problem from Hackerrank
# https://www.hackerrank.com/challenges/no-prefix-set/problem
#
# Problem: No Prefix Set
#
# Description:
# Given a set of strings, determine if it forms a "GOOD SET" where no
# string is a prefix of another. If a prefix conflict exists, output
# "BAD SET" and the offending string.
#
# Input:
# - First line: n (number of strings)
# - Next n lines: one string per line
#
# Output:
# - "GOOD SET" if no string is a prefix of another
# - "BAD SET" followed by the first string causing the conflict
#
# Approach:
# - Build a Trie incrementally
# - For each new string, check:
#   1. If we pass through a word-end node (existing string is prefix of new)
#   2. If current string ends at non-leaf node (new string is prefix of existing)

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
        # result = s
        # while len(tmp.child) > 0:
        #     for key in tmp.child:
        #         result += key
        #         tmp = tmp.child[key]
        #         break

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

### contacts (Hackerrank)

```python
# Problem from Hackerrank
# https://www.hackerrank.com/challenges/contacts/problem
#
# Problem: Contacts
#
# Description:
# Implement a contact list with two operations:
# - add <name>: Add a contact name to the list
# - find <partial>: Count contacts starting with the given partial name
#
# Input:
# - First line: n (number of operations)
# - Next n lines: operation and argument
#
# Output:
# - For each "find" operation: number of contacts with matching prefix
#
# Approach:
# - Use a Trie where each node maintains a count of words passing through it
# - When adding, increment count at each node along the path
# - When finding, traverse to prefix node and return its count
# - Time complexity: O(L) for both add and find operations

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

### 1129_Consistency_Checker (LightOJ)

```python
# Problem from LightOJ
# http://lightoj.com/volume_showproblem.php?problem=1129
#
# Problem: Consistency Checker (LightOJ 1129)
#
# Description:
# A phone directory is consistent if no phone number is a prefix of another.
# Given a list of phone numbers, check if the directory is consistent.
#
# Input:
# - First line: T (test cases)
# - For each test case:
#   - n (number of phone numbers)
#   - n phone numbers (digits only)
#
# Output:
# - For each test case: "Case X: YES" if consistent, "Case X: NO" otherwise
#
# Approach:
# - Build a Trie with phone numbers
# - Check for prefix conflicts during insertion:
#   - If a complete number exists along the path (prefix of current)
#   - If current number ends at a non-leaf (current is prefix of existing)


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

### 1224_DNA_Prefix (LightOJ)

```python
# Problem from LightOJ
# http://lightoj.com/volume_showproblem.php?problem=1224
#
# Problem: DNA Prefix (LightOJ 1224)
#
# Description:
# Given a set of DNA strings, find the maximum "prefix score". The prefix
# score of a set is defined as (length of common prefix) * (number of strings).
# Find the maximum score achievable by any subset sharing a common prefix.
#
# Input:
# - First line: T (test cases)
# - For each test case:
#   - n (number of DNA strings)
#   - n DNA strings (containing A, C, G, T)
#
# Output:
# - For each test case: "Case X: max_score"
#
# Approach:
# - Build a Trie with DNA strings
# - Each node tracks cumulative "weight" = sum of depths of strings passing through
# - Maximum weight at any node represents the best prefix score
# - Weight calculation: depth * count_of_strings_through_node


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

### Product_Repository (Custom)

```python
# Problem: Product Suggestions (Amazon/LeetCode style)
#
# Description:
# Given a product repository and a customer search query, suggest up to 3
# products for each prefix of the query (starting from 2 characters).
# Products should be suggested in lexicographical order.
#
# Input:
# - numProducts: number of products in repository
# - repository: list of product names
# - customerQuery: search string
#
# Output:
# - List of lists: for each prefix of query (length 2 onwards), up to 3
#   lexicographically smallest matching products
#
# Approach:
# - Build a Trie from all product names
# - For each query prefix, find the Trie node
# - Extract up to 3 words from that subtree in lexicographical order
# - Uses DFS with sorted child keys for ordered traversal


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
    # WRITE YOUR CODE HERE
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


# numProducts = 5
# repository = ['mobile', 'mouse', 'moneypot', 'monitor', 'mouspad']
# customerQuery = 'mouse'


numProducts = 5
repository = ['code', 'codePhone', 'coddle', 'coddles', 'codes']
customerQuery = 'coddle'


print(threeProductSuggestions(numProducts, repository, customerQuery))
```

### 5792_Diccionário Portuñol (ICPC Archive)

```python
# Problem from icpcarchive
# https://icpcarchive.ecs.baylor.edu/index.php?option=onlinejudge&page=show_problem&problem=3803
#
# Problem: Diccionario Portunol (ICPC Archive 5792)
#
# Description:
# Create a "Portunol" dictionary by combining Portuguese and Spanish words.
# A Portunol word is formed by taking a prefix of a Portuguese word and
# appending a suffix of a Spanish word. Count the number of distinct
# Portunol words that can be formed.
#
# Input:
# - Multiple test cases until P=S=0
# - P (Portuguese words), S (Spanish words)
# - P Portuguese words
# - S Spanish words
#
# Output:
# - For each test case: number of distinct Portunol words
#
# Approach:
# - Use a Trie to store and count unique combined words
# - For each Portuguese word prefix (length 1 to full length)
# - Combine with each Spanish word suffix (all possible suffixes)
# - Add to Trie and count only new unique words

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

