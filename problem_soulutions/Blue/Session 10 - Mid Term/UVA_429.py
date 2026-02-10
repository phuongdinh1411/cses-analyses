#  Problem from UVA
#  https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=370
#
# Problem Name: Word Transformation (UVA 429)
#
# Problem Description:
# Given a dictionary of words and pairs of words, find the minimum number
# of single-character transformations needed to change one word into another.
# A valid transformation changes exactly one character while keeping the
# resulting word in the dictionary.
#
# Input Format:
# - N: number of test cases
# - For each test case:
#   - Dictionary words (one per line) until '*'
#   - Query pairs (start_word end_word) until blank line
#
# Output Format:
# - For each query: start_word end_word min_transformations
#
# Key Approach/Algorithm:
# - Build a graph where nodes are dictionary words
# - Connect two words with an edge if they differ by exactly one character
# - Use BFS to find shortest path between query words


from collections import deque


def bfs(start, end, graph, word_to_idx):
    """BFS to find shortest path from start word to end word."""
    if start not in word_to_idx or end not in word_to_idx:
        return -1

    start_idx = word_to_idx[start]
    end_idx = word_to_idx[end]

    if start_idx == end_idx:
        return 0

    n = len(graph)
    dist = [-1] * n
    dist[start_idx] = 0

    queue = deque([start_idx])
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                if v == end_idx:
                    return dist[v]
                queue.append(v)

    return -1


def differs_by_one(word1, word2):
    """Check if two words differ by exactly one character."""
    if len(word1) != len(word2):
        return False
    diff = 0
    for c1, c2 in zip(word1, word2):
        # Fixed: Use != instead of 'is not' for string comparison
        if c1 != c2:
            diff += 1
            if diff > 1:
                return False
    return diff == 1


def solution():
    N = int(input().strip())

    for tc in range(N):
        dictionary = []
        while True:
            new_word = input().strip()
            if not new_word:
                continue
            if new_word == '*':
                break
            dictionary.append(new_word)

        queries = []
        while True:
            try:
                new_query = input().strip()
            except:
                break
            if not new_query:
                break
            queries.append(new_query.split())

        # Build word to index mapping
        word_to_idx = {word: i for i, word in enumerate(dictionary)}
        n_words = len(dictionary)

        # Build graph: connect words that differ by one character
        graph = [[] for _ in range(n_words)]
        for i in range(n_words):
            for j in range(i + 1, n_words):
                if differs_by_one(dictionary[i], dictionary[j]):
                    graph[i].append(j)
                    graph[j].append(i)

        # Process queries
        for query in queries:
            start_word, end_word = query[0], query[1]
            result = bfs(start_word, end_word, graph, word_to_idx)
            print(start_word, end_word, result)

        if tc < N - 1:
            print()


solution()
