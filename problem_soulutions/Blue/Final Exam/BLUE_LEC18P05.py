# BLUE_LEC18P05
"""
Problem: Phone List / Prefix-Free Set Validation (Trie)

Description:
Given a list of phone numbers, determine if the list is "consistent" - meaning no phone
number is a prefix of another phone number. For example, if the list contains both
"911" and "9111234", it is inconsistent because "911" is a prefix of "9111234".

This problem is also known as:
- Phone List (UVa)
- Consistent Phone Numbers
- Prefix-Free Code Validation

Input Format:
- Line 1: Integer T (number of test cases)
- For each test case:
  - Line 1: Integer N (number of phone numbers)
  - Next N lines: One phone number string per line

Output Format:
- For each test case: "YES" if the list is consistent (no prefix conflicts), "NO" otherwise

Algorithm/Approach:
1. Use a Trie (prefix tree) data structure
2. For each phone number, insert it into the trie character by character
3. While inserting, check for prefix conflicts:
   - If we pass through a node marked as end of a word -> current number has a prefix in the set
   - If we reach the end but the node has children -> current number is a prefix of another
4. If any conflict is found, output "NO"; otherwise "YES"
"""


class Node:
    def __init__(self):
        self.is_end_of_word = False
        self.children = {}


def add_word(root, s):
    """
    Add a word to the trie. Return False if prefix conflict detected.
    """
    node = root
    for ch in s:
        if ch not in node.children:
            node.children[ch] = Node()
        node = node.children[ch]
        # Check if current prefix is already a complete word
        if node.is_end_of_word:
            return False

    # Check if this word is a prefix of an existing word
    if node.children:
        return False

    node.is_end_of_word = True
    return True


def solution():
    tc = int(input())
    for _ in range(tc):
        root = Node()
        n = int(input())
        is_consistent = True

        for i in range(n):
            s = input().strip()
            if is_consistent:
                result = add_word(root, s)
                if not result:
                    is_consistent = False
                    print('NO')
                    # Fixed: Consume remaining input lines for this test case
                    for j in range(i + 1, n):
                        input()
                    break

        if is_consistent:
            print('YES')


solution()
