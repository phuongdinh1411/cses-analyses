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
