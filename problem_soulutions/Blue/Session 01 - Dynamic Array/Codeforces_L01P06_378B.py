# Problem from Codeforces
# http://codeforces.com/problemset/problem/378/B
#
# Problem: Semifinals
#
# Two semifinals of a race, each with n participants. The top n participants
# overall (by finish time) will qualify for the finals. For each position in
# each semifinal, determine if that racer has a chance to qualify (1) or
# definitely won't qualify (0).
#
# The first ceil(n/2) from each semifinal are guaranteed to qualify. The
# remaining spots depend on cross-semifinal comparisons.
#
# Input:
# - Line 1: Integer n (participants per semifinal)
# - Next n lines: a[i] b[i] (finish times for position i in semifinals A and B)
#
# Output: Two lines of n characters each (0 or 1), representing qualification
#         chances for each position in semifinal A and B respectively


def calc_chances_matrix(_n, _a, _b):
    k = n // 2
    chances_matrix = [[1] * k + [0] * (n - k) for j in range(2)]

    last_a = k - 1
    last_b = k - 1
    if n % 2 == 1:
        if _a[k] < _b[k]:
            last_a += 1
            chances_matrix[0][k] = 1
        else:
            last_b += 1
            chances_matrix[1][k] = 1
    while last_a < n - 1 and last_b < n - 1:
        if _a[last_a + 1] < _b[n - (last_a + 1) - 1]:
            last_a += 1
            chances_matrix[0][last_a] = 1
        elif _b[last_b + 1] < _a[n - (last_b + 1) - 1]:
            last_b += 1
            chances_matrix[1][last_b] = 1
        else:
            break
    return chances_matrix


n = int(input())
a, b = [], []
for i in range(n):
    ai, bi = map(int, input().split())
    a.append(ai)
    b.append(bi)

print(*calc_chances_matrix(n, a, b)[0], sep='')
print(*calc_chances_matrix(n, a, b)[1], sep='')
