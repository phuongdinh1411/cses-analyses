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
