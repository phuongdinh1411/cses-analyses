# Problem: Find the Median
#
# Problem Description:
# Given an array of N integers, find the median value.
# For an array sorted in ascending order, the median is the middle element.
# If N is odd, it's the element at index N/2 (0-indexed after sorting).
#
# Input Format:
# - First line: N (number of elements)
# - Second line: N space-separated integers
#
# Output Format:
# - A single integer: the median of the array
#
# Key Approach/Algorithm:
# - Sort the array in ascending order
# - Return the element at index N//2

def solution():
    n = int(input())
    ar = list(map(int, input().strip().split()))
    ar.sort()
    mid_index = n//2

    print(ar[mid_index])


solution()
