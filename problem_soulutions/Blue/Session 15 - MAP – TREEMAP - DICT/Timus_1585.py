# Problem from ACM TIMUS
# http://acm.timus.ru/problem.aspx?space=1&num=1585
#
# Problem: Penguins
#
# Description:
# A group of penguins have names. Find the most frequently occurring name
# among all the penguins. If there's a tie, return the name that appeared
# first with the maximum count.
#
# Input:
# - First line: n (number of penguins)
# - Next n lines: name of each penguin
#
# Output:
# - The most common penguin name
#
# Approach:
# - Use a dictionary to count occurrences of each name
# - Track the most frequent name while iterating
# - Simple hash map frequency counting problem


def solution():
    penguins = {}
    n_penguins = int(input())
    most_numerous_number = 0
    most_numerous_penguin = ''
    for i in range(n_penguins):
        penguin = input().strip()
        if penguins.get(penguin) is None:
            penguins[penguin] = 1
        else:
            penguins[penguin] += 1
        if penguins[penguin] > most_numerous_number:
            most_numerous_number = penguins[penguin]
            most_numerous_penguin = penguin

    print(most_numerous_penguin)


solution()
