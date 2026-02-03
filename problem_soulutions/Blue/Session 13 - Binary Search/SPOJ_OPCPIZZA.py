# Problem from SPOJ
# https://www.spoj.com/problems/OPCPIZZA/
#
# Problem Name: OPC's Pizza (SPOJ OPCPIZZA)
#
# Problem Description:
# At a party, N friends want to share pizzas. Each pizza costs M dollars and
# must be bought by exactly two friends. Each friend has a certain amount of
# money. Find the maximum number of pizzas that can be bought.
#
# Input Format:
# - T: number of test cases
# - For each test case:
#   - N M: number of friends, pizza cost
#   - N integers: amount of money each friend has
#
# Output Format:
# - Maximum number of pizzas that can be bought
#
# Key Approach/Algorithm:
# - Two-pointer technique on sorted array
# - Sort friends by money amount
# - Use left and right pointers to find pairs summing to exactly M
# - Move pointers based on whether sum is less, equal, or greater than M


def solution():
    T = int(input())
    for i in range(T):
        n, m = map(int, input().strip().split())
        friends = list(map(int, input().strip().split()))
        friends.sort()
        left = 0
        right = n - 1
        total = 0
        while left < right:
            if friends[left] + friends[right] == m:
                left += 1
                right -= 1
                total += 1
            if friends[left] + friends[right] > m:
                right -= 1
            if friends[left] + friends[right] < m:
                left += 1

        print(total)


solution()


