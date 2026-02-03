#  Problem from Hackerrank
#  https://www.hackerrank.com/challenges/camelcase/problem
#
# Problem Name: CamelCase
#
# Problem Description:
# Given a string in camelCase format (first word starts with lowercase,
# subsequent words start with uppercase), count the number of words.
#
# Input Format:
# - A single line containing a camelCase string
#
# Output Format:
# - A single integer: the number of words in the string
#
# Key Approach/Algorithm:
# - Start with count = 1 (for the first word)
# - Iterate through each character
# - If character is uppercase (ASCII < 97), increment counter
# - Each uppercase letter marks the start of a new word


def solution():

    s = input().strip()
    counter = 1
    for c in s:
        if ord(c) < 97:
            counter += 1

    print(counter)


solution()
