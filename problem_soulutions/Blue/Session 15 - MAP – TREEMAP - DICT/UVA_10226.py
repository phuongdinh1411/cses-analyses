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
# - Blank line between test cases
#
# Approach:
# - Use dictionary to count occurrences of each tree species
# - Calculate percentage = (count / total) * 100
# - Sort keys alphabetically for output
# - Fixed: Use format specifier to ensure exactly 4 decimal places


def solution():
    n = int(input())
    input()  # Consume blank line after number of cases

    for case in range(n):
        population = {}
        total = 0

        while True:
            try:
                tree_name = input()
                if not tree_name:
                    break
            except EOFError:
                break

            population[tree_name] = population.get(tree_name, 0) + 1
            total += 1

        # Output results in alphabetical order
        for tree in sorted(population.keys()):
            percentage = population[tree] * 100 / total
            # Fixed: Use format specifier to guarantee 4 decimal places
            print(f'{tree} {percentage:.4f}')

        # Fixed: Print blank line between test cases (but not after the last one)
        if case < n - 1:
            print()


solution()
