# Problem from Codeforces
# http://codeforces.com/problemset/problem/1152/C
#
# Problem Name: Neko does Maths
#
# Problem Description:
# Given two positive integers a and b, find the smallest non-negative integer k
# such that LCM(a+k, b+k) is minimized. LCM is the Least Common Multiple.
#
# Input Format:
# - Single line with two integers a and b
#
# Output Format:
# - Single integer k that minimizes LCM(a+k, b+k)
#
# Key Approach/Algorithm:
# - Key insight: GCD(a+k, b+k) = GCD(a+k, |b-a|) = GCD(b+k, |b-a|)
# - The GCD must be a divisor of |a-b|
# - Iterate through all divisors of |a-b| (up to sqrt(|a-b|))
# - For each divisor d, find smallest k such that (a+k) % d == 0
# - Track the k that gives minimum LCM
from math import sqrt

INF = 1e18


def gcd(x, y):
    if y == 0:
        return x
    else:
        return gcd(y, x % y)


def solution():
    atmp, btmp = map(int, input().strip().split())
    a = max(atmp, btmp)
    b = min(atmp, btmp)
    k = 0

    delta = a - b
    min_lcm = INF

    if delta == 0:
        print(0)
        exit(0)

    range_gcd = int(sqrt(delta)) + 1
    for i in range(1, range_gcd):
        if delta % i == 0:
            k, min_lcm = getk(a, b, i, k, min_lcm)
            k, min_lcm = getk(a, b, delta / i, k, min_lcm)

    print('{0:.0f}'.format(k))


def getk(a, b, i, k, min_lcm):
    current_k = 0
    if b % i > 0:
        current_k = ((b // i) + 1) * i - b
    lcm = (a + current_k) * (b + current_k) / i
    if lcm < min_lcm:
        min_lcm = lcm
        k = current_k
    return k, min_lcm


solution()
