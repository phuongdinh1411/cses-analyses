# Problem: Pangram
#
# Problem Description:
# A pangram is a sentence that contains every letter of the alphabet at least once.
# Given a string, determine if it is a pangram.
#
# Input Format:
# - First line: N (length of the string)
# - Second line: a string of N characters
#
# Output Format:
# - "YES" if the string is a pangram, "NO" otherwise
#
# Key Approach/Algorithm:
# - Use a boolean array of size 26 to track presence of each letter
# - Convert each alphabetic character to index (0-25) regardless of case
# - Skip non-alphabetic characters
# - If all 26 positions are True, it's a pangram


def solution():
    num_of_chars = int(input())
    checking_string = input().strip()

    # Track which letters (a-z) have been seen
    seen = [False] * 26

    for char in checking_string:
        # Fixed: Only process alphabetic characters
        if char.isalpha():
            # Convert to lowercase and get index (0-25)
            index = ord(char.lower()) - ord('a')
            seen[index] = True

    # Check if all letters are present
    if all(seen):
        print('YES')
    else:
        print('NO')


solution()
