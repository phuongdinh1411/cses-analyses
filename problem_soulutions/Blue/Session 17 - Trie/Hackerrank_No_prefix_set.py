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
