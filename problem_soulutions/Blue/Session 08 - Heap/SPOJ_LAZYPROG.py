#  Problem from SPOJ
#  https://www.spoj.com/problems/LAZYPROG/
#
# Problem: LAZYPROG - Lazy Programmer
#
# A lazy programmer has N projects with deadlines. Each project i has:
# - a[i]: cost per unit time to speed up (dollars/hour)
# - b[i]: time needed to complete at normal speed (hours)
# - d[i]: deadline (hours from now)
#
# He can pay to speed up any project. Find the minimum total cost to meet
# all deadlines.
#
# Input:
# - Line 1: T (test cases)
# - For each test case:
#   - Line 1: N (number of projects)
#   - Next N lines: a b d for each project
#
# Output: Minimum cost (2 decimal places)
#
# Approach: Sort by deadline, use heap to always speed up cheapest project first


import heapq


class Project:
    def __init__(self, a, b, d):
        self.a = a
        self.b = b
        self.d = d

    def __lt__(self, other):
        return self.a > other.a


def solution():
    t = int(input())

    for i in range(t):
        sum_money = 0
        initial_time = 0
        priority_queue = []
        projects = []
        n = int(input())
        for j in range(n):
            a, b, d = map(int, input().strip().split())
            projects.append(Project(a, b, d))
        projects.sort(key=lambda x: x.d, reverse=False)

        for j in range(n):
            initial_time += projects[j].b
            heapq.heappush(priority_queue, projects[j])
            if initial_time <= projects[j].d:
                continue
            while True:
                pop_project = heapq.heappop(priority_queue)
                if initial_time - pop_project.b <= projects[j].d:
                    pop_project.b -= initial_time-projects[j].d
                    sum_money += (initial_time-projects[j].d) / pop_project.a
                    initial_time = projects[j].d
                    heapq.heappush(priority_queue, pop_project)
                    break

                else:
                    sum_money += pop_project.b / pop_project.a
                    initial_time -= pop_project.b

        print("{0:.2f}".format(sum_money))


solution()
