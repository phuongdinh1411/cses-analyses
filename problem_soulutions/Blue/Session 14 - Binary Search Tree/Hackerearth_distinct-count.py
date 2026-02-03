#  Problem from Hackerearth
#  https://www.hackerearth.com/fr/practice/data-structures/trees/binary-search-tree/practice-problems/algorithm/distinct-count/
#
# Problem Name: Distinct Count
#
# Problem Description:
# Given an array of N integers and a target X, determine if the number of
# distinct elements equals X, is less than X, or is greater than X.
#
# Input Format:
# - T: number of test cases
# - For each test case:
#   - N X: size of array and target count
#   - N integers (the array)
#
# Output Format:
# - "Good" if distinct count equals X
# - "Bad" if distinct count is less than X
# - "Average" if distinct count is greater than X
#
# Key Approach/Algorithm:
# - Use a set to count distinct elements in O(n)
# - Compare set size with X to determine result


def check_distinct(_n, _x, _a):
    distinct_set = set(_a)
    # for i in range(_n):
    #     distinct_set.add(_a[i])
    if len(distinct_set) == _x:
        return 'Good'
    if len(distinct_set) < _x:
        return 'Bad'
    return 'Average'


def solution():
    T = int(input())
    for i in range(T):
        N, X = map(int, input().strip().split())
        A = list(map(int, input().strip().split()))
        print(check_distinct(N, X, A))


solution()
