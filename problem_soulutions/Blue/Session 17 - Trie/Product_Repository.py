# Problem: Product Suggestions (Amazon/LeetCode style)
#
# Description:
# Given a product repository and a customer search query, suggest up to 3
# products for each prefix of the query (starting from 2 characters).
# Products should be suggested in lexicographical order.
#
# Input:
# - numProducts: number of products in repository
# - repository: list of product names
# - customerQuery: search string
#
# Output:
# - List of lists: for each prefix of query (length 2 onwards), up to 3
#   lexicographically smallest matching products
#
# Approach:
# - Build a Trie from all product names
# - For each query prefix, find the Trie node
# - Extract up to 3 words from that subtree in lexicographical order
# - Uses DFS with sorted child keys for ordered traversal


class Node:
    def __init__(self):
        self.child = dict()
        self.word_count = 0


def add_word(root, s):
    tmp = root
    for ch in s:
        if ch not in tmp.child:
            tmp.child[ch] = Node()

        tmp = tmp.child[ch]
    tmp.word_count += 1


def find_word(root, s):
    tmp = root
    for ch in s:
        if ch not in tmp.child:
            return []
        tmp = tmp.child[ch]
    return tmp


def extract_words(found_node):
    result = []

    if found_node.child:
        if found_node.word_count > 0:
            result.append('')
            if len(result) >= 3:
                return result

        current_keys = sorted(list(found_node.child.keys()))
        for k in current_keys:
            for s in extract_words(found_node.child[k]):
                result.append(k + s)
                if len(result) >= 3:
                    return result
    else:
        result.append('')
    return result


def threeProductSuggestions(numProducts, repository, customerQuery):
    # WRITE YOUR CODE HERE
    root = Node()
    for i in range(numProducts):
        add_word(root, repository[i])

    results = []
    for i in range(2, len(customerQuery) + 1):
        current_query = customerQuery[:i]
        found_node = find_word(root, current_query)
        if not found_node:
            break

        result = extract_words(found_node)
        for k in range(len(result)):
            result[k] = current_query + result[k]

        results.append(result)

    return results


# numProducts = 5
# repository = ['mobile', 'mouse', 'moneypot', 'monitor', 'mouspad']
# customerQuery = 'mouse'


numProducts = 5
repository = ['code', 'codePhone', 'coddle', 'coddles', 'codes']
customerQuery = 'coddle'


print(threeProductSuggestions(numProducts, repository, customerQuery))
