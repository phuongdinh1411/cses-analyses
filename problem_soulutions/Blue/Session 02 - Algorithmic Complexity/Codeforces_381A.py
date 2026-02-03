# Problem from Codeforces
# http://codeforces.com/contest/381/problem/A
#
# Problem: Sereja and Dima
#
# n cards are laid out in a row, each with a value. Sereja and Dima play a
# game where they take turns picking cards. On each turn, a player can take
# either the leftmost or rightmost card. Both players play optimally (always
# pick the card with the higher value). Sereja goes first.
#
# Calculate the final scores of both players.
#
# Input:
# - Line 1: Integer n (number of cards)
# - Line 2: n integers (card values)
#
# Output: Two integers - Sereja's score and Dima's score
#
# Approach: Two-pointer simulation from both ends

n = int(input())
cards = list(map(int, input().split()))

Sereja = 0
Dima = 0

left = 0
right = n - 1

while True:
    if cards[left] > cards[right]:
        Sereja += cards[left]
        left += 1
    else:
        Sereja += cards[right]
        right -= 1
    if left > right:
        break
    if cards[left] > cards[right]:
        Dima += cards[left]
        left += 1
    else:
        Dima += cards[right]
        right -= 1
    if left > right:
        break

print(Sereja, Dima, sep=' ')
