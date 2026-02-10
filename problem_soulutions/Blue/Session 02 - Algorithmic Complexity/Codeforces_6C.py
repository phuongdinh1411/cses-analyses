# Problem from Codeforces
# http://codeforces.com/problemset/problem/6/C
#
# Problem: Alice, Bob and Chocolate
#
# n chocolate bars are lined up. Alice starts eating from the left side,
# Bob starts from the right side. They eat simultaneously and continuously.
# Each bar i takes t[i] seconds to eat. When they meet (or would overlap),
# they stop. If they finish a chocolate at the same time and there's one
# bar left, Alice gets it (Alice has priority on ties).
#
# Determine how many chocolates each person eats.
#
# Input:
# - Line 1: Integer n (number of chocolates)
# - Line 2: n integers (time to eat each chocolate)
#
# Output: Two integers - chocolates eaten by Alice and Bob
#
# Approach: Two-pointer simulation with cumulative time tracking
# - Track Alice's total time eating from left
# - Track Bob's total time eating from right
# - Alice gets the chocolate if her cumulative time <= Bob's (tie goes to Alice)

n = int(input())
t = list(map(int, input().split()))

alice_count = 0
bob_count = 0
alice_time = 0
bob_time = 0

left = 0
right = n - 1

while left <= right:
    if alice_time <= bob_time:
        # Alice eats the next chocolate (tie goes to Alice)
        alice_time += t[left]
        alice_count += 1
        left += 1
    else:
        # Bob eats the next chocolate
        bob_time += t[right]
        bob_count += 1
        right -= 1

print(alice_count, bob_count)
