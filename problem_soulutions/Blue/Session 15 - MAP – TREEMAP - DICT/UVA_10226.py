# Problem from UVA
# https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1167
#
# Problem: Hardwood Species (UVA 10226)
#
# Description:
# A census of trees in a forest has been conducted. Given a list of tree species,
# calculate what percentage of the total forest each species represents.
# Output results in alphabetical order.
#
# Input:
# - First line: number of test cases
# - For each test case: list of tree names (one per line), separated by blank lines
#
# Output:
# - For each test case: each tree species followed by its percentage (4 decimal places)
# - Species listed in alphabetical order
#
# Approach:
# - Use dictionary to count occurrences of each tree species
# - Calculate percentage = (count / total) * 100
# - Sort keys alphabetically for output

# import sys


# sys.stdin = open("file.txt", "r")


def solution():
    n = int(input())
    input()

    for i in range(n):
        population = {}
        total = 0
        while True:
            try:
                new_line = input()
                if not new_line:
                    break
            except:
                break
            if population.get(new_line) is None:
                population[new_line] = 1
            else:
                population[new_line] += 1

            total += 1
        sorted_list = sorted(population.keys())

        for tree in sorted_list:
            print(tree + ' ' + str(round(population.get(tree) * 100 / total, 4)))


solution()
