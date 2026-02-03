# Problem from Codeforces
# http://codeforces.com/problemset/problem/451/B
#
# Problem: Sort the Array
#
# Given an array of n distinct integers, determine if you can sort it in
# ascending order by reversing exactly one contiguous segment. If possible,
# output "yes" and the segment boundaries. Otherwise, output "no".
#
# Input:
# - Line 1: Integer n (array size)
# - Line 2: n distinct integers (array elements)
#
# Output:
# - Line 1: "yes" or "no"
# - Line 2 (if yes): Start and end indices (1-based) of segment to reverse
#
# Approach: Find the single decreasing segment, check if reversing it sorts the array

n = int(input())
a = list(map(int, input().split()))

found_decreasing_segment = False
start_segment = 0
end_segment = 0

i = 0
while i < n - 1:
    if a[i] > a[i + 1]:
        if found_decreasing_segment:
            print('no')
            exit()
        start_segment = i
        found_decreasing_segment = True
        while i < n - 1 and a[i] > a[i + 1]:
            i += 1
        end_segment = i
        if (end_segment < n - 1 and a[start_segment] > a[end_segment + 1]) \
                or (start_segment > 0 and a[end_segment] < a[start_segment - 1]):
            print('no')
            exit()
    else:
        i += 1

print('yes')
print(start_segment + 1, end_segment + 1, sep=' ')
