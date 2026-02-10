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
# Approach: Use two heaps - one for top ceil(n/3) ratings (min-heap), another
#           for candidates (max-heap). Keep balance as reviews are added.


import heapq


def solution():
    top_reviews = []      # Min-heap: stores top ceil(n/3) ratings
    candidate_reviews = []  # Max-heap (negated): stores remaining ratings
    N = int(input())
    results = []
    num_reviews = 0

    for _ in range(N):
        command = input().strip()
        if command.startswith('1'):
            num_reviews += 1
            new_review = int(command.split()[1])

            # Fixed: Use ceiling division for target size
            # ceil(n/3) = (n + 2) // 3
            target_top_size = (num_reviews + 2) // 3

            if len(top_reviews) < target_top_size:
                # Need to add to top_reviews
                if not candidate_reviews or new_review >= -candidate_reviews[0]:
                    heapq.heappush(top_reviews, new_review)
                else:
                    # Move largest from candidates to top, add new to candidates
                    heapq.heappush(top_reviews, -heapq.heappop(candidate_reviews))
                    heapq.heappush(candidate_reviews, -new_review)
            else:
                # top_reviews is at capacity
                if top_reviews and new_review > top_reviews[0]:
                    # New review belongs in top, move smallest from top to candidates
                    heapq.heappush(candidate_reviews, -heapq.heappop(top_reviews))
                    heapq.heappush(top_reviews, new_review)
                else:
                    heapq.heappush(candidate_reviews, -new_review)
        else:
            # Query
            if top_reviews:
                results.append(top_reviews[0])
            else:
                results.append('No reviews yet')

    print(*results, sep='\n')


solution()
