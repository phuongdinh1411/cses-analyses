# Problem from CodeChef
# https://www.codechef.com/problems/RRATING
#
# Problem: Restaurant Rating
#
# A restaurant receives reviews with ratings. After each review, they want
# to display the rating at the top 1/3 position (ceiling). For example, if
# there are 5 reviews, show the rating at position ceil(5/3) = 2 from top.
#
# Operations:
# - "1 x": Add a review with rating x
# - "2": Query the rating at top 1/3 position (or "No reviews yet" if empty)
#
# Input:
# - Line 1: N (number of operations)
# - Next N lines: Operations as described above
#
# Output: For each query (type 2), print the answer
#
# Approach: Use two heaps - one for top 1/3 ratings (min-heap), another for
#           candidates (max-heap). Keep balance as reviews are added.


import heapq


def solution():
    top_reviews = []
    candidate_reviews = []
    N = int(input())
    results = []
    num_of_reviews = 0
    for i in range(N):
        command = input().strip()
        if command.startswith('1'):
            num_of_reviews += 1
            new_review = int(command.split()[1])
            if len(top_reviews) < num_of_reviews // 3:
                if len(candidate_reviews) < 0 or new_review > -candidate_reviews[0]:
                    heapq.heappush(top_reviews, new_review)
                else:
                    heapq.heappush(top_reviews, -candidate_reviews[0])
                    heapq.heappop(candidate_reviews)
                    heapq.heappush(candidate_reviews, -new_review)
            else:
                if len(top_reviews) > 0 and new_review > top_reviews[0]:
                    heapq.heappush(candidate_reviews, -top_reviews[0])
                    heapq.heappop(top_reviews)
                    heapq.heappush(top_reviews, new_review)
                else:
                    heapq.heappush(candidate_reviews, -new_review)
        else:
            if len(top_reviews) > 0:
                results.append(top_reviews[0])
            else:
                results.append('No reviews yet')

    print(*results, sep='\n')


solution()
