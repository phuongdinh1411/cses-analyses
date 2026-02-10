#  Problem from SPOJ
#  https://www.spoj.com/problems/LAZYPROG/
#
# Problem: LAZYPROG - Lazy Programmer
#
# A lazy programmer has N projects with deadlines. Each project i has:
# - a[i]: cost per unit time to speed up (dollars/hour saved)
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
# when we're running late. Greedy: prefer speeding up projects with lower cost/hour.


import heapq


class Project:
    def __init__(self, cost_per_hour, duration, deadline):
        self.cost = cost_per_hour  # Cost per hour saved
        self.duration = duration    # Remaining duration
        self.deadline = deadline

    def __lt__(self, other):
        # Fixed: Min-heap by cost (lower cost = higher priority for speeding up)
        return self.cost < other.cost


def solution():
    t = int(input())

    for _ in range(t):
        total_cost = 0.0
        current_time = 0
        available_projects = []  # Min-heap of projects we can speed up
        projects = []

        n = int(input())
        for _ in range(n):
            a, b, d = map(int, input().strip().split())
            projects.append(Project(a, b, d))

        # Sort by deadline (earliest first)
        projects.sort(key=lambda x: x.deadline)

        for project in projects:
            current_time += project.duration
            heapq.heappush(available_projects, project)

            # If we're past the deadline, speed up the cheapest projects
            while current_time > project.deadline and available_projects:
                cheapest = heapq.heappop(available_projects)
                time_over = current_time - project.deadline

                if cheapest.duration >= time_over:
                    # Speed up this project partially
                    total_cost += time_over * cheapest.cost
                    cheapest.duration -= time_over
                    current_time = project.deadline
                    if cheapest.duration > 0:
                        heapq.heappush(available_projects, cheapest)
                else:
                    # Speed up this project completely
                    total_cost += cheapest.duration * cheapest.cost
                    current_time -= cheapest.duration

        print("{0:.2f}".format(total_cost))


solution()
