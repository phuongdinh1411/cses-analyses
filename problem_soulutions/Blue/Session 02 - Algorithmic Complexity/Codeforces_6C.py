# Problem from Codeforces
# http://codeforces.com/problemset/problem/6/C
#
# Problem: Alice, Bob and Chocolate
#
# n chocolate bars are lined up. Alice starts eating from the left side,
# Bob starts from the right side. They eat simultaneously and continuously.
# Each bar i takes t[i] seconds to eat. When they meet (or would overlap),
# they stop. If they finish a chocolate at the same time and there's one
# bar left, Alice gets it.
#
# Determine how many chocolates each person eats.
#
# Input:
# - Line 1: Integer n (number of chocolates)
# - Line 2: n integers (time to eat each chocolate)
#
# Output: Two integers - chocolates eaten by Alice and Bob
#
# Approach: Two-pointer simulation with time tracking

n = int(input())
t = list(map(int, input().split()))

alice_eating_index = 0
bob_eating_index = n - 1
while True:
    if alice_eating_index >= bob_eating_index - 1:
        break
    if t[alice_eating_index] > t[bob_eating_index]:
        t[alice_eating_index] -= t[bob_eating_index]
        bob_eating_index -= 1
    elif t[alice_eating_index] < t[bob_eating_index]:
        t[bob_eating_index] -= t[alice_eating_index]
        alice_eating_index += 1
    else:
        if bob_eating_index - alice_eating_index == 2:
            alice_eating_index += 1
        else:
            alice_eating_index += 1
            bob_eating_index -= 1


print(alice_eating_index + 1, n - alice_eating_index - 1)
