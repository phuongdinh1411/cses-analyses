# Problem from Codeforces
# http://codeforces.com/problemset/problem/691/A
#
# Problem: Jacket
#
# A jacket has n buttons arranged in a row. Each button is either fastened (1)
# or unfastened (0). A jacket is considered "properly fastened" if:
# - When n = 1: the button must be fastened
# - When n > 1: exactly one button must be unfastened
#
# Input:
# - Line 1: Integer n (number of buttons)
# - Line 2: n integers (0 or 1)
#
# Output: "YES" if properly fastened, "NO" otherwise
#
# Example: n=3, buttons=[1,0,1] → "YES" (exactly one unfastened)


def check_jacket(_a, _n):
    un_fastened = 0
    if _n == 1:
        if _a[0] == 0:
            return 'NO'
        else:
            return 'YES'
    else:
        for i in range(_n):
            un_fastened += (1 - _a[i])
            if un_fastened > 1:
                return 'NO'
        if un_fastened == 0:
            return 'NO'
        else:
            return 'YES'


n = int(input())
a = list(map(int, input().split()))
print(check_jacket(a, n))


