# BLUE_LEC18P01
"""
Problem: Three Distinct Permutations of Sorted Array

Description:
Given an array of N integers, determine if it is possible to create at least 3 distinct
permutations that, when sorted by values, produce different index mappings. If possible,
output "YES" and print 3 such permutations; otherwise output "NO".

The key insight is that we need duplicate values in the array to create different permutations:
- If a value appears exactly 2 times, we can swap their positions (2 arrangements)
- If a value appears 3+ times, we get more arrangements
- To get 3 distinct permutations, we need either:
  * One value appearing 4+ times (can create 3+ arrangements from one value)
  * Two values each appearing exactly 2 times (2 * 2 = 4 >= 3 arrangements)

Input Format:
- Line 1: Integer N (size of array)
- Line 2: N space-separated integers (the array elements)

Output Format:
- If not possible: "NO"
- If possible: "YES" followed by 3 lines, each containing a permutation
  (1-indexed positions that would sort the array)

Algorithm/Approach:
1. Track positions of each unique value using a dictionary
2. Check if conditions for 3 permutations are met:
   - Two values with exactly 2 occurrences each, OR
   - One value with 4+ occurrences
3. Generate permutations by swapping positions of duplicate values
"""


def solution():
    N = int(input())

    tasks = list(map(int, input().split()))

    markers = {}

    for i in range(N):
        if markers.get(tasks[i]) is None:
            markers[tasks[i]] = [1]
        markers[tasks[i]].append(i)

    possible = False
    possible_count = 1

    duplications = []
    duplicated_keys = []
    for key, marker in markers.items():
        if len(marker) == 3:
            possible_count *= 2
            duplications.append(marker)
            duplicated_keys.append(key)
            if possible_count >= 3:
                possible = True
                break

        elif len(marker) >= 4:
            possible = True
            duplications = [marker]
            duplicated_keys = [key]
            break

    if not possible:
        print('NO')
        return

    print('YES')
    tasks.sort()

    if len(duplications) == 2:

        for i in range(N):
            print(markers[tasks[i]][markers[tasks[i]][0]] + 1, end=' ')
            if markers[tasks[i]][0] == len(markers[tasks[i]]) - 1:
                markers[tasks[i]][0] = 1
            else:
                markers[tasks[i]][0] += 1
        markers[duplicated_keys[0]][2], markers[duplicated_keys[0]][1] = markers[duplicated_keys[0]][1], \
                                                                         markers[duplicated_keys[0]][2]

        for marker in markers.values():
            marker[0] = 1
        print()
        for i in range(N):
            print(markers[tasks[i]][markers[tasks[i]][0]] + 1, end=' ')
            if markers[tasks[i]][0] == len(markers[tasks[i]]) - 1:
                markers[tasks[i]][0] = 1
            else:
                markers[tasks[i]][0] += 1
        for marker in markers.values():
            marker[0] = 1
        print()

        markers[duplicated_keys[1]][2], markers[duplicated_keys[1]][1] = markers[duplicated_keys[1]][1], \
                                                                         markers[duplicated_keys[1]][2]

        for i in range(N):
            print(markers[tasks[i]][markers[tasks[i]][0]] + 1, end=' ')
            if markers[tasks[i]][0] == len(markers[tasks[i]]) - 1:
                markers[tasks[i]][0] = 1
            else:
                markers[tasks[i]][0] += 1

    if len(duplications) == 1:
        for i in range(N):
            print(markers[tasks[i]][markers[tasks[i]][0]] + 1, end=' ')
            if markers[tasks[i]][0] == len(markers[tasks[i]]) - 1:
                markers[tasks[i]][0] = 1
            else:
                markers[tasks[i]][0] += 1

        print()
        for marker in markers.values():
            marker[0] = 1
        markers[duplicated_keys[0]][2], markers[duplicated_keys[0]][1] = markers[duplicated_keys[0]][1], \
                                                                         markers[duplicated_keys[0]][2]

        for i in range(N):
            print(markers[tasks[i]][markers[tasks[i]][0]] + 1, end=' ')
            if markers[tasks[i]][0] == len(markers[tasks[i]]) - 1:
                markers[tasks[i]][0] = 1
            else:
                markers[tasks[i]][0] += 1

        print()
        for marker in markers.values():
            marker[0] = 1
        markers[duplicated_keys[0]][2], markers[duplicated_keys[0]][3] = markers[duplicated_keys[0]][3], \
                                                                         markers[duplicated_keys[0]][2]

        for i in range(N):
            print(markers[tasks[i]][markers[tasks[i]][0]] + 1, end=' ')
            if markers[tasks[i]][0] == len(markers[tasks[i]]) - 1:
                markers[tasks[i]][0] = 1
            else:
                markers[tasks[i]][0] += 1


solution()
