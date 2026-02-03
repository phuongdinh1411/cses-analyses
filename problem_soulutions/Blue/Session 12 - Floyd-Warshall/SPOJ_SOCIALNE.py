# Problem from SPOJ
# https://www.spoj.com/problems/SOCIALNE/
#
# Problem Name: Social Network
#
# Problem Description:
# Given a social network represented as a friendship matrix, find the person
# who can make the most new friends through existing friends (friends-of-friends).
# A person can become friends with someone who is a friend of their friend
# but not already their direct friend.
#
# Input Format:
# - T: number of test cases
# - For each test case:
#   - M x M matrix where 'Y' means friendship exists, 'N' means no friendship
#
# Output Format:
# - For each test case: person_index max_new_friends
#   (0-indexed person who gains most new friends through friend-of-friend connections)
#
# Key Approach/Algorithm:
# - Modified Floyd-Warshall concept for transitive closure
# - For each person i, count people j where i and j are not friends directly
#   but share a common friend k (matrix[i][k]='Y' and matrix[k][j]='Y')
# - Track which person gains the most potential new friends


def floyd_warshall(M, matrix):
    dist = [[False] * M for i in range(M)]
    for i in range(M):
        n_friend = 0
        for j in range(M):
            if matrix[i][j] == 'Y':
                n_friend += 1
                dist[i][j] = True

    n_more_friends = [0 for i in range(M)]
    for k in range(M):
        for i in range(M):
            for j in range(M):
                if not dist[i][j] and i != j and matrix[i][k] == 'Y' and matrix[k][j] == 'Y':
                    dist[i][j] = True
                    n_more_friends[i] += 1

    max_new_friends = n_more_friends[0]
    most_pop_person = 0
    for i in range(1, M):
        if n_more_friends[i] > max_new_friends:
            max_new_friends = n_more_friends[i]
            most_pop_person = i
    print(most_pop_person, max_new_friends)


def solution():
    T = int(input())
    for i in range(T):
        matrix = []
        first_line = input().strip()
        M = len(first_line)
        matrix.append(first_line)
        for j in range(M - 1):
            matrix.append(input().strip())

        floyd_warshall(M, matrix)


solution()


