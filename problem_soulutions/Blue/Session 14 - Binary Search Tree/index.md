---
layout: simple
title: "Binary Search Tree"
permalink: /problem_soulutions/Blue/Session 14 - Binary Search Tree/
---

# Binary Search Tree

This session covers Binary Search Tree (BST) data structure, including insertion, deletion, search operations, and balanced trees.

## Problems

### Han Solo and Lazer Gun

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

#### Problem Statement

Han Solo is at position (x0, y0) and needs to shoot n stormtroopers. A single laser shot can kill all stormtroopers on the same ray from Han. Find the minimum number of shots needed to eliminate all stormtroopers.

#### Input Format
- First line: n x0 y0 (number of stormtroopers, Han's position)
- Next n lines: x y (coordinates of each stormtrooper)

#### Output Format
- Minimum number of shots (distinct rays) needed

#### Example
```
Input:
4 0 0
1 1
2 2
2 0
-1 -1

Output:
2
```
Han is at (0,0). Stormtroopers at (1,1) and (2,2) are on the same ray (same slope). Stormtrooper at (2,0) is on a different ray. Stormtrooper at (-1,-1) is on the same ray as (1,1) and (2,2). So 2 shots needed: one for the diagonal, one for horizontal.

#### Solution

##### Approach
Two points are on the same ray if they have the same angle from origin. For each stormtrooper, compute angle (or slope) relative to Han's position. Use a set to count distinct angles/slopes. Stormtroopers with same slope are on the same ray.

##### Python Solution

```python
from math import gcd


def solution():
    n, x0, y0 = map(int, input().strip().split())
    rays = set()

    for _ in range(n):
        x, y = map(int, input().strip().split())
        dx, dy = x - x0, y - y0

        # Normalize direction using GCD for exact comparison
        g = gcd(abs(dx), abs(dy)) or 1
        dx, dy = dx // g, dy // g

        # Handle sign normalization for opposite directions on same ray
        if dx < 0 or (dx == 0 and dy < 0):
            dx, dy = -dx, -dy

        rays.add((dx, dy))

    print(len(rays))


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n)
- **Space Complexity:** O(n)

---

### Thor

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

#### Problem Statement

Simulate a notification system with n applications. Three operations:
1. Type 1 x: application x generates a notification
2. Type 2 x: read all notifications from application x
3. Type 3 t: read first t notifications in order

After each operation, output the current number of unread notifications.

#### Input Format
- First line: n q (number of applications, number of operations)
- Next q lines: type x (operation type and parameter)

#### Output Format
- q lines: number of unread notifications after each operation

#### Example
```
Input:
3 5
1 1
1 2
1 3
2 2
3 2

Output:
1
2
3
2
0
```
After op 1 (app 1 notifies): 1 unread. After op 2 (app 2 notifies): 2 unread. After op 3 (app 3 notifies): 3 unread. After op 4 (read all from app 2): 2 unread. After op 5 (read first 2 in order): 0 unread (notifications 1,2,3 existed, reading first 2 removes them all since app 2's was already read).

#### Solution

##### Approach
Use sets to track unread notifications per application. Use a queue to track notification order for type 3 operations. For type 2: clear all notifications from specific app. For type 3: process notifications in order up to given index.

##### Python Solution

```python
from collections import deque


def solution():
    n, num_ops = map(int, input().strip().split())
    app_notifications = [set() for _ in range(n + 1)]
    notification_queue = deque()
    unread_count = 0
    notification_id = 1
    processed_count = 0

    for _ in range(num_ops):
        op_type, param = map(int, input().split())

        if op_type == 1:  # New notification from app
            app_notifications[param].add(notification_id)
            notification_queue.append((notification_id, param))
            notification_id += 1
            unread_count += 1

        elif op_type == 2:  # Read all from specific app
            unread_count -= len(app_notifications[param])
            app_notifications[param].clear()

        elif op_type == 3:  # Read first t notifications in order
            while processed_count < param:
                noti_id, app_id = notification_queue.popleft()
                if noti_id in app_notifications[app_id]:
                    unread_count -= 1
                    app_notifications[app_id].discard(noti_id)
                processed_count += 1

        print(unread_count)


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(q) amortized
- **Space Complexity:** O(q)

---

### Distinct Count

#### Problem Information
- **Source:** HackerEarth
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given an array of N integers and a target X, determine if the number of distinct elements equals X, is less than X, or is greater than X.

#### Input Format
- T: number of test cases
- For each test case:
  - N X: size of array and target count
  - N integers (the array)

#### Output Format
- "Good" if distinct count equals X
- "Bad" if distinct count is less than X
- "Average" if distinct count is greater than X

#### Example
```
Input:
3
5 3
1 2 3 2 1
4 4
1 2 3 4
3 5
1 1 1

Output:
Good
Good
Bad
```
Test 1: Array [1,2,3,2,1] has 3 distinct elements, equals X=3 -> Good. Test 2: Array [1,2,3,4] has 4 distinct elements, equals X=4 -> Good. Test 3: Array [1,1,1] has 1 distinct element, less than X=5 -> Bad.

#### Solution

##### Approach
Use a set to count distinct elements in O(n). Compare set size with X to determine result.

##### Python Solution

```python
def check_distinct(arr, target):
    distinct_count = len(set(arr))
    if distinct_count == target:
        return 'Good'
    return 'Bad' if distinct_count < target else 'Average'


def solution():
    t = int(input())
    for _ in range(t):
        n, x = map(int, input().strip().split())
        arr = list(map(int, input().strip().split()))
        print(check_distinct(arr, x))


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(T * N)
- **Space Complexity:** O(N)

---

### Minimum Loss

#### Problem Information
- **Source:** HackerRank
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Lauren wants to buy a house and sell it later. She has predicted house prices for n years. She must buy before selling (buy year < sell year). She can only afford to make a loss (buy price > sell price). Find the minimum possible loss she must incur.

#### Input Format
- n: number of years
- n integers: predicted house prices (all distinct)

#### Output Format
- Minimum loss (buy_price - sell_price where buy_price > sell_price)

#### Example
```
Input:
5
20 7 8 2 5

Output:
2
```
Prices over 5 years: [20, 7, 8, 2, 5]. Lauren must buy before selling and incur a loss. Options: buy at 20, sell at 7 (loss=13); buy at 20, sell at 8 (loss=12); buy at 8, sell at 2 (loss=6); buy at 8, sell at 5 (loss=3); buy at 7, sell at 5 (loss=2). Minimum loss is 2.

#### Solution

##### Approach
Build a BST as we process prices in chronological order. For each new price (potential sell price), find the smallest price greater than it in the BST (which represents a valid buy price from past). The loss is (buy_price - current_price). Track minimum loss across all valid pairs.

##### Python Solution

```python
import bisect


def minimum_loss(prices):
    """Find minimum loss by buying and selling house."""
    INF = float('inf')
    min_loss = INF
    sorted_prices = []

    for price in prices:
        # Find the smallest price greater than current (valid past buy price)
        pos = bisect.bisect_right(sorted_prices, price)

        if pos < len(sorted_prices):
            loss = sorted_prices[pos] - price
            min_loss = min(min_loss, loss)

        # Insert current price into sorted list
        bisect.insort(sorted_prices, price)

    return min_loss


if __name__ == '__main__':
    n = int(input())
    prices = list(map(int, input().rstrip().split()))
    print(minimum_loss(prices))
```

##### Complexity Analysis
- **Time Complexity:** O(n log n) average, O(n^2) worst case for unbalanced BST
- **Space Complexity:** O(n)

---

### Monk and his Friends

#### Problem Information
- **Source:** HackerEarth
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Monk is waiting for his friends in a classroom. N friends are already inside. M more friends arrive one by one. When a friend arrives, check if someone with the same ID is already in the class. After checking, the friend enters.

#### Input Format
- T: number of test cases
- For each test case:
  - N M: friends already inside, friends arriving
  - N+M integers: IDs (first N already inside, next M arriving)

#### Output Format
- For each arriving friend: "YES" if duplicate exists, "NO" otherwise

#### Example
```
Input:
1
3 2
1 2 3 1 4

Output:
YES
NO
```
Friends with IDs [1,2,3] are already inside. First arriving friend has ID 1 (duplicate exists) -> YES. After checking, ID 1 is added again (now two with ID 1). Second arriving friend has ID 4 (no duplicate) -> NO.

#### Solution

##### Approach
Use a set to store IDs of friends inside the class. For each arriving friend, check if ID exists in set. Add the arriving friend's ID to the set after checking.

##### Python Solution

```python
def solution():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().strip().split())
        ids = list(map(int, input().strip().split()))

        present = set(ids[:n])

        for student_id in ids[n:]:
            print('YES' if student_id in present else 'NO')
            present.add(student_id)


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(T * (N + M))
- **Space Complexity:** O(N + M)

---

### History Exam

#### Problem Information
- **Source:** ACM TIMUS
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 64MB

#### Problem Statement

A student memorized n historical years for an exam. The exam has m questions asking about specific years. Count how many questions the student can answer correctly (i.e., how many exam years match memorized years).

#### Input Format
- n: number of years the student memorized
- n lines: memorized years (one per line)
- m: number of exam questions
- m lines: years asked in exam (one per line)

#### Output Format
- Number of correct answers (exam years that match memorized years)

#### Example
```
Input:
4
1917
1939
1945
1941
3
1945
1942
1917

Output:
2
```
Student memorized years: [1917, 1939, 1945, 1941]. Exam questions ask about: 1945 (memorized - correct), 1942 (not memorized - wrong), 1917 (memorized - correct). Total: 2 correct answers.

#### Solution

##### Approach
Build a Binary Search Tree from memorized years. For each exam question, search the BST. Count successful searches.

##### Python Solution

```python
def solution():
    n = int(input().strip())
    memorized = {int(input()) for _ in range(n)}

    m = int(input().strip())
    correct = sum(1 for _ in range(m) if int(input()) in memorized)

    print(correct)


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n log n + m log n) average case
- **Space Complexity:** O(n)

---

### Andy's First Dictionary

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

#### Problem Statement

Andy is making a dictionary from a text. Extract all distinct words from the input, convert to lowercase, and output them in alphabetical order. Words consist only of alphabetic characters.

#### Input Format
- Multiple lines of text containing words and non-alphabetic characters

#### Output Format
- All distinct words in lowercase, sorted alphabetically (one per line)

#### Example
```
Input:
Adventures in Disneyland
Two dogs and a cat.
END.

Output:
a
adventures
and
cat
disneyland
dogs
end
in
two
```
All unique words extracted, converted to lowercase, and sorted alphabetically.

#### Solution

##### Approach
Parse input to extract words (alphabetic sequences only). Convert to lowercase. Use a BST (or set) to store unique words. In-order traversal of BST gives sorted output.

##### Python Solution

```python
import re


def solution():
    words = set()

    while True:
        try:
            line = input().strip()
            # Extract alphabetic words and convert to lowercase
            line_words = re.findall(r'[A-Za-z]+', line)
            words.update(word.lower() for word in line_words)
        except:
            break

    for word in sorted(words):
        print(word)


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(W log W) where W is total words
- **Space Complexity:** O(U) where U is unique words

---

### Andy's Second Dictionary

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

#### Problem Statement

Similar to Andy's First Dictionary, but now words can contain hyphens. A word split across lines with a hyphen at end should be merged. Extract all distinct words, convert to lowercase, output alphabetically.

#### Input Format
- Multiple lines of text
- Words may contain hyphens
- A word ending with hyphen at end of line continues on next line

#### Output Format
- All distinct words in lowercase, sorted alphabetically (one per line)

#### Example
```
Input:
Well-known scientists from
around the globe gath-
ered to discuss.

Output:
around
discuss
from
gathered
globe
scientists
the
to
well-known
```
"gath-" at end of line 2 continues with "ered" on line 3 to form "gathered". "well-known" is kept as a hyphenated word since the hyphen is not at line end.

#### Solution

##### Approach
Parse input handling hyphenated words and line-continuation hyphens. Track incomplete words (ending with hyphen at line end). Merge with next line's first word. Use BST for unique sorted storage. In-order traversal outputs sorted words.

##### Python Solution

```python
import re


def solution():
    words = set()
    incomplete_word = ''

    while True:
        try:
            line = input().strip()
            # Extract words with hyphens
            line_words = [w.lower() for w in re.findall(r'[A-Za-z-]+', line) if w]
        except:
            break

        if not line_words:
            continue

        # Handle continuation from previous line
        if incomplete_word:
            line_words[0] = incomplete_word[:-1] + line_words[0]
            incomplete_word = ''

        # Check if last word continues to next line
        if line_words[-1].endswith('-'):
            incomplete_word = line_words[-1]
            line_words = line_words[:-1]

        words.update(line_words)

    for word in sorted(words):
        print(word)


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(W log W) where W is total words
- **Space Complexity:** O(U) where U is unique words
