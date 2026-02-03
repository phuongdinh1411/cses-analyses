# Problem from UVA
# https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=12822
#
# Problem Name: Solve It (UVA 10341)
#
# Problem Description:
# Solve the equation: p*e^(-x) + q*sin(x) + r*cos(x) + s*tan(x) + t*x^2 + u = 0
# for x in the range [0, 1]. The function is monotonically decreasing in this range.
#
# Input Format:
# - Multiple lines, each with 6 integers: p q r s t u
#
# Output Format:
# - For each line: the root x with 4 decimal places, or "No solution"
#
# Key Approach/Algorithm:
# - Binary search on the answer in range [0, 1]
# - Since function is monotonically decreasing, if f(mid) * f(lo) < 0,
#   the root is in [lo, mid], otherwise in [mid, hi]
# - Continue until result is within epsilon tolerance
# import sys

import math

epsilon = math.pow(10, -9)


def calc_result(p, q, r, s, t, u, x):

    return p * math.exp(-x) + q * math.sin(x) + r * math.cos(x) + s * math.tan(x) + t * math.pow(x, 2) + u


def solution():
    while True:
        try:
            p, q, r, s, t, u= map(int, input().strip().split())
            lo, hi = 0, 1
            if -epsilon < calc_result(p, q, r, s, t, u, lo) < epsilon:
                print(lo)
                continue
            if -epsilon < calc_result(p, q, r, s, t, u, hi) < epsilon:
                print(hi)
                continue

            has_solution = False
            for i in range(1000):
                x = (lo + hi) / 2
                result = calc_result(p, q, r, s, t, u, x)

                if -epsilon < result < epsilon:
                    print('{0:.4f}'.format(x))
                    has_solution = True
                    break
                if result * calc_result(p, q, r, s, t, u, lo) < 0:
                    hi = x
                elif result * calc_result(p, q, r, s, t, u, hi) < 0:
                    lo = x
            if not has_solution:
                print('No solution')

        except Exception as e:
            break


solution()

