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
# - Start with count = 1 (for the first word) if string is non-empty
# - Iterate through each character
# - If character is uppercase, increment counter
# - Each uppercase letter marks the start of a new word


def solution():
    s = input().strip()

    # Fixed: Handle empty string edge case
    if not s:
        print(0)
        return

    counter = 1
    for c in s:
        # Fixed: Use isupper() instead of ASCII comparison to properly detect uppercase
        if c.isupper():
            counter += 1

    print(counter)


solution()
