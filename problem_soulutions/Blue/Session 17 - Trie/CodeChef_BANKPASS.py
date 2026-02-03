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
