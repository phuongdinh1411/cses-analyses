# Problem from SPOJ
# https://www.spoj.com/problems/ARBITRAG/
#
# Problem Name: Arbitrage
#
# Problem Description:
# Given currency exchange rates between different currencies, determine if
# arbitrage is possible. Arbitrage means starting with some currency and
# exchanging through a sequence of currencies to end up with more of the
# original currency than you started with.
#
# Input Format:
# - Multiple test cases until n=0
# - For each test case:
#   - n: number of currencies
#   - n currency names
#   - m: number of exchange rates
#   - m lines: currency1 rate currency2 (exchange currency1 to currency2 at given rate)
#
# Output Format:
# - "Case X: Yes" if arbitrage is possible, "Case X: No" otherwise
#
# Key Approach/Algorithm:
# - Modified Floyd-Warshall for product maximization instead of sum minimization
# - matrix[i][j] = max(matrix[i][j], matrix[i][k] * matrix[k][j])
# - If any diagonal element > 1 after algorithm, arbitrage exists (cycle with gain)

INF = float(1e9)
# sys.stdout = open("file.txt", "w+")


def floyd_warshall(M, matrix):

    for k in range(M):
        for i in range(M):
            for j in range(M):
                if matrix[i][j] < matrix[i][k] * matrix[k][j]:
                    matrix[i][j] = matrix[i][k] * matrix[k][j]
    for i in range(M):
        if matrix[i][i] > 1:
            return 'Yes'

    return 'No'


def solution():
    n_case = 1
    while True:
        line = input().strip()
        while not line:
            line = input().strip()
        M = int(line)
        if M == 0:
            break

        my_dict = {}
        for i in range(M):
            my_dict[input().strip()] = i

        exchanges = int(input().strip())
        matrix = [[0.0] * M for i in range(M)]
        for i in range(exchanges):
            c1, rate, c2 = map(str, input().strip().split())
            matrix[my_dict[c1]][my_dict[c2]] = float(rate)

        print('Case ' + str(n_case) + ': ' + floyd_warshall(M, matrix))
        n_case += 1


solution()


