# Problem: Soldier and Bananas (Codeforces 546A)
#
# Problem Description:
# A soldier wants to buy w bananas. The cost of bananas is progressive:
# the 1st banana costs k dollars, 2nd costs 2*k, 3rd costs 3*k, and so on.
# The soldier has n dollars. How much more money does he need to borrow?
#
# Input Format:
# - Single line with three integers: k n w
#   - k: base cost of first banana
#   - n: dollars the soldier has
#   - w: number of bananas to buy
#
# Output Format:
# - Single integer: amount to borrow (0 if soldier has enough)
#
# Key Approach/Algorithm:
# - Total cost = k * (1 + 2 + ... + w) = k * w * (w + 1) / 2
# - Amount to borrow = max(0, total_cost - n)

def solution():
    k, n, w = map(int, input().strip().split())

    result = int((w + 1) * w * k / 2 - n)
    if result < 0:
        result = 0

    print(result)


solution()
