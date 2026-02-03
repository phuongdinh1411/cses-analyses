# Problem from Codeforces
# http://codeforces.com/problemset/problem/26/B
#
# Problem Name: Regular Bracket Sequence
#
# Problem Description:
# Given a bracket sequence consisting only of '(' and ')' characters,
# find the length of the longest regular (properly nested) bracket subsequence.
#
# Input Format:
# - A single string containing only '(' and ')' characters
# - Length up to 10^6
#
# Output Format:
# - A single integer: the length of the longest regular bracket subsequence
#
# Key Approach/Algorithm:
# - Greedy approach using a counter (position)
# - Track opening brackets with a counter
# - For each closing bracket, if there's a matching opening bracket, add 2 to total
# - If no matching opening bracket, skip the closing bracket


def solution():
    s = input().strip()
    pos = 0
    total = 0
    for c in s:
        if c == '(':
            pos += 1
        else:
            pos -= 1
            if pos >= 0:
                total += 2
            else:
                pos += 1

    print(total)


solution()


