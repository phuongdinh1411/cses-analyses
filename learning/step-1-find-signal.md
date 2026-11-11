# Step 1 — Find Signal: Heap (Data Structures & Algorithms)

## The 5 Highest-Leverage Resources

### 1. 📘 CLRS — Chapter 6: Heapsort & Priority Queues
- **Type:** Textbook
- **Why:** Canonical academic treatment. Covers binary heap properties, heapify, build-heap, heap sort with full proofs.
- **Teaches:** Heap structure, heapify correctness, build-heap linear time proof, heap sort
- **Best for:** Visual-logical thinkers who want rock-solid foundations
- **Difficulty:** Intermediate
- **How to use:** Read Ch6 actively — draw every figure by hand, prove the height-of-heap property yourself
- **⚠️ Warning:** Don't get lost in appendix math. Focus only on Ch6 and §6.5 (Priority Queue)

### 2. 🎬 NeetCode.io — Heap / Priority Queue Playlist
- **Type:** Video + Practice (Free)
- **Why:** Interview-focused. Explains heap patterns with visual animations. Maps directly to problem patterns.
- **Teaches:** Min/max-heap, Python heapq, top-K patterns, two-heap trick
- **Best for:** Coding interview preppers, visual learners
- **Difficulty:** Beginner → Intermediate
- **How to use:** Watch, pause before solution reveal, code yourself, then compare
- **⚠️ Warning:** Don't just watch — code every problem or retention drops to near zero

### 3. 💻 LeetCode Heap Problem Set — Curated 20-problem ladder
- **Type:** Practice Platform
- **Why:** Heaps have ~6 recurring patterns. 20 well-chosen problems covers all of them.
- **Teaches:** Top-K, K-way merge, scheduling, sliding window, median, greedy
- **Best for:** Anyone preparing for FAANG-level interviews
- **Difficulty:** Beginner → Advanced
- **How to use:** Easy (5) → Medium (12) → Hard (3). Time yourself after first 5.
- **⚠️ Warning:** Avoid random picking — stick to a curated ladder

### 4. 🌐 CS Visualgo — Heap Visualization (visualgo.net/en/heap)
- **Type:** Interactive Visual Tool (Free)
- **Why:** Watching heap rebalance live builds an accurate mental model before coding.
- **Teaches:** Binary heap structure, sift-up, sift-down, index math
- **Best for:** Visual learners, beginners
- **Difficulty:** Beginner
- **How to use:** Predict each step *before* clicking "next"
- **⚠️ Warning:** Don't use passively — always predict first, then verify

### 5. 📄 Python `heapq` docs + Greg Plaxton's Lecture Notes
- **Type:** Reference Docs
- **Why:** `heapq` is the tool you'll use in every interview. Knowing its quirks saves debugging time.
- **Teaches:** heappush, heappop, nlargest/nsmallest, lazy deletion, max-heap workaround (-val)
- **Best for:** Practical coders who want concept → working code fast
- **Difficulty:** Beginner → Advanced
- **How to use:** Read while solving LeetCode problems. Plaxton's notes for advanced variants after mastering binary heaps.
- **⚠️ Warning:** Don't spend time on Fibonacci heaps unless studying for PhD-level work

---

## Recommended Order
1. visualgo.net        ← Build mental model FIRST (Day 1, 30 min)
2. CLRS Chapter 6      ← Solidify theory + proofs (Day 1–2)
3. NeetCode playlist   ← Learn interview patterns visually (Day 3–4)
4. LeetCode ladder     ← Apply and build muscle memory (Day 4–7)
5. Python heapq docs   ← Reference as needed during coding

---

## 7-Day Learning Path

| Day | Goal | Activity | Time |
|-----|------|----------|------|
| 1 | Build mental model | Visualgo animations + CLRS §6.1–6.2 | 2 hrs |
| 2 | Solidify theory | CLRS §6.3–6.5 + implement binary heap from scratch | 2 hrs |
| 3 | Learn patterns | NeetCode: Kth Largest, Top K Frequent, Last Stone Weight | 2 hrs |
| 4 | Learn more patterns | NeetCode: K Closest Points, Task Scheduler, Design Twitter Feed | 2 hrs |
| 5 | Apply Easy/Medium | LeetCode: 703, 1046, 215, 347, 973, 621, 355 | 2.5 hrs |
| 6 | Apply Medium/Hard | LeetCode: 23, 295, 502, 1675 | 2.5 hrs |
| 7 | Review + gaps | Re-solve 3 hard problems, write your own cheat sheet | 1.5 hrs |

**Total: ~14.5 hours → strong heap foundation + interview-ready**
