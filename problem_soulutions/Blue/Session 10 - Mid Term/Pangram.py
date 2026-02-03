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
# - Convert each character to index (0-25) regardless of case
# - Mark the corresponding index as True
# - If all 26 positions are True, it's a pangram

def solution():
    num_of_chars = int(input())
    checking_string = input().strip()

    checking_array = [False for i in range(26)]

    for i in range(num_of_chars):
        char_index = ord(checking_string[i]) - 65
        if char_index >= 26:
            char_index = ord(checking_string[i]) - 97

        checking_array[char_index] = True

    for i in range(26):
        if not checking_array[i]:
            print('NO')
            return
    print('YES')


solution()
