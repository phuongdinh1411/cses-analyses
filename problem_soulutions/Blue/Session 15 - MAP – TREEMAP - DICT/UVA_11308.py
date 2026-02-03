# Problem from UVA
# https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=2283
#
# Problem: Bankrupt Baker (UVA 11308)
#
# Description:
# A baker has recipe binders with ingredients and recipes. Given a budget,
# find which recipes can be made within budget. Output affordable recipes
# sorted by cost (then alphabetically if tied).
#
# Input:
# - Number of binders
# - For each binder:
#   - Binder name
#   - m (ingredients), n (recipes), b (budget)
#   - m lines of ingredient name and price
#   - n recipes, each with name, number of ingredients, and ingredient quantities
#
# Output:
# - For each binder: binder name (uppercase), then affordable recipes
#   sorted by cost then name, or "Too expensive!" if none affordable
#
# Approach:
# - Use dictionary to map ingredient names to prices
# - Calculate total cost for each recipe
# - Filter and sort recipes within budget

# import sys


# sys.stdin = open("file.txt", "r")
class Recipe:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

    def __lt__(self, other):
        if self.cost < other.cost:
            return True
        elif self.cost == other.cost:
            return self.name < other.name
        return False


def solution():
    binders = int(input())
    for i in range(binders):
        binder_name = input().strip().upper()
        m, n, b = map(int, input().strip().split())
        ingredients = {}
        for j in range(m):
            ingredient_name, ingredient_price = map(str, input().split())
            ingredients[ingredient_name] = int(ingredient_price)
        print(binder_name)
        can_makes = []
        for j in range(n):
            recipe_name = input().strip()
            k = int(input())
            total_cost = 0
            for x in range(k):
                ingredient_name, quantity = map(str, input().split())
                quantity = int(quantity)
                total_cost += quantity * ingredients[ingredient_name]

            if total_cost <= b:
                can_makes.append(Recipe(recipe_name, total_cost))

        if len(can_makes) == 0:
            print('Too expensive!')
        else:
            can_makes.sort()
            n_can_makes = len(can_makes)
            for cm in range(n_can_makes):
                print(can_makes[cm].name)
        print()


solution()
