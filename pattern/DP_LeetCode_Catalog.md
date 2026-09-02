---
layout: simple
title: "LeetCode DP — Categorized by Technique"
permalink: /pattern/dp-leetcode-catalog
---

# LeetCode Dynamic Programming — Categorized by Technique

> Every problem from the official [LeetCode *Dynamic Programming* list](https://leetcode.com/problem-list/dynamic-programming/) (676 problems), grouped by the **core DP technique** each one exercises. For a from-scratch teaching guide of the techniques themselves, see [DP Patterns](/pattern/dp).

**Total:** 676 problems — 14 Easy · 327 Medium · 335 Hard.

## Technique Index

| # | Technique | Problems | Core recurrence |
|---|-----------|:--------:|-----------------|
| 1 | [Linear Sequence DP (1D)](#linear-sequence-dp-1d) | 172 | `dp[i] = f(dp[i-1], dp[i-2], ...)` |
| 2 | [Grid / Matrix Path DP (2D)](#grid-matrix-path-dp-2d) | 53 | `dp[i][j] = grid[i][j] + best(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])` |
| 3 | [Knapsack / Subset-Sum](#knapsack-subset-sum) | 58 | 0/1: `dp[c] = max(dp[c], dp[c-w]+v)` iterate capacity **descending**. Unbounded: iterate **ascending**. |
| 4 | [Longest Increasing Subsequence (LIS)](#longest-increasing-subsequence-lis) | 24 | `dp[i] = 1 + max(dp[j] for j<i if a[j]<a[i])`; or maintain `tails[]` + `bisect`. |
| 5 | [Two-Sequence / String-Edit DP](#two-sequence-string-edit-dp) | 29 | `dp[i][j] = dp[i-1][j-1]+1` on match, else `combine(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`. |
| 6 | [Palindrome DP](#palindrome-dp) | 18 | `dp[i][j] = (s[i]==s[j]) && dp[i+1][j-1]`; longest-pal-subseq `dp[i][j]=dp[i+1][j-1]+2` on match. |
| 7 | [Interval / Range DP](#interval-range-dp) | 39 | `dp[i][j] = min/max over k in (i,j) of dp[i][k] + dp[k][j] + cost(i,k,j)` |
| 8 | [Stock / State-Machine DP](#stock-state-machine-dp) | 10 | `hold[i]=max(hold[i-1], cash[i-1]-price)`, `cash[i]=max(cash[i-1], hold[i-1]+price-fee)` |
| 9 | [Tree DP](#tree-dp) | 36 | `dfs(node) -> (take, skip)`; `take = node.val + sum(skip_child)`, `skip = sum(max(take,skip)_child)`. |
| 10 | [Digit DP](#digit-dp) | 28 | `dp[pos][tight][state]` = sum over next digit `d in [0 .. (tight? N[pos]:9)]`. |
| 11 | [Bitmask DP](#bitmask-dp) | 44 | `dp[mask] = best over i in mask of dp[mask ^ (1<<i)] + cost(...)` |
| 12 | [Counting / Combinatorial DP](#counting-combinatorial-dp) | 85 | `dp[i] = sum of dp[j]` over valid predecessors; combine with multiplication for independent choices. |
| 13 | [Kadane / Max-Subarray DP](#kadane-max-subarray-dp) | 15 | `cur = max(a[i], cur + a[i]); best = max(best, cur)` (track min too for products). |
| 14 | [Game Theory (Minimax) DP](#game-theory-minimax-dp) | 15 | `dp[i][j] = max(a[i]-dp[i+1][j], a[j]-dp[i][j-1])` (current player maximizes own margin). |
| 15 | [DP on Graphs (shortest-path / DAG)](#dp-on-graphs-shortest-path-dag) | 22 | `dp[v] = combine over edges (u->v) of dp[u] + w(u,v)`; process in topo order for DAGs. |
| 16 | [Probability / Expectation DP](#probability-expectation-dp) | 8 | `E[state] = sum over outcomes p(outcome) · (reward + E[next])` |
| 17 | [Other DP](#other-dp) | 20 | Varies. |

---

## Linear Sequence DP (1D)

**172 problems.** State is a single index `i`; the answer at `i` depends on a constant number of earlier indices. The workhorse family — climbing stairs, house robber, decode ways, word break, jump game all live here.

- **Recognize it when:** You walk a 1D array/string once and each position's optimum is a small combine of a few predecessors.
- **Recurrence:** `dp[i] = f(dp[i-1], dp[i-2], ...)`
- **Complexity:** Time `O(n)` (or `O(n·k)` with a window `k`), space `O(n)` reducible to `O(1)` when only last few states matter.

| # | Problem | Difficulty | Core idea |
|---|---------|:----------:|-----------|
| 70 | [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) | Easy | dp[i]=dp[i-1]+dp[i-2] |
| 338 | [Counting Bits](https://leetcode.com/problems/counting-bits/) | Easy | dp[i]=dp[i>>1]+(i&1) |
| 509 | [Fibonacci Number](https://leetcode.com/problems/fibonacci-number/) | Easy | dp[i]=dp[i-1]+dp[i-2] |
| 746 | [Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/) | Easy | dp[i]=cost+min(dp[i-1],dp[i-2]) |
| 1137 | [N-th Tribonacci Number](https://leetcode.com/problems/n-th-tribonacci-number/) | Easy | dp[i]=sum of three previous |
| 1668 | [Maximum Repeating Substring](https://leetcode.com/problems/maximum-repeating-substring/) | Easy | count consecutive repeats of word |
| 2900 | [Longest Unequal Adjacent Groups Subsequence I](https://leetcode.com/problems/longest-unequal-adjacent-groups-subsequence-i/) | Easy | dp longest alternating-group subsequence |
| 45 | [Jump Game II](https://leetcode.com/problems/jump-game-ii/) | Medium | min jumps reach index i (greedy DP) |
| 55 | [Jump Game](https://leetcode.com/problems/jump-game/) | Medium | reachable index from previous jumps |
| 91 | [Decode Ways](https://leetcode.com/problems/decode-ways/) | Medium | dp[i] from dp[i-1],dp[i-2] valid decodes |
| 139 | [Word Break](https://leetcode.com/problems/word-break/) | Medium | dp[i] true if dp[j] and s[j:i] in dict |
| 198 | [House Robber](https://leetcode.com/problems/house-robber/) | Medium | dp[i]=max(dp[i-1],dp[i-2]+a) |
| 213 | [House Robber II](https://leetcode.com/problems/house-robber-ii/) | Medium | rob linear, two circular cases |
| 256 | [Paint House](https://leetcode.com/problems/paint-house/) | Medium | dp[i][color] min cost different adjacent |
| 264 | [Ugly Number II](https://leetcode.com/problems/ugly-number-ii/) | Medium | dp[n] merge three pointers times 2,3,5 |
| 276 | [Paint Fence](https://leetcode.com/problems/paint-fence/) | Medium | same/diff color counts from previous post |
| 313 | [Super Ugly Number](https://leetcode.com/problems/super-ugly-number/) | Medium | k pointers merge next ugly number |
| 343 | [Integer Break](https://leetcode.com/problems/integer-break/) | Medium | dp[n]=max over j of j*dp[n-j] |
| 396 | [Rotate Function](https://leetcode.com/problems/rotate-function/) | Medium | F(k)=F(k-1)+sum-n*A[n-k] rolling transition |
| 397 | [Integer Replacement](https://leetcode.com/problems/integer-replacement/) | Medium | dp[n] min ops from n/2 or n+-1 |
| 413 | [Arithmetic Slices](https://leetcode.com/problems/arithmetic-slices/) | Medium | dp[i]+=dp[i-1] if diff equal |
| 418 | [Sentence Screen Fitting](https://leetcode.com/problems/sentence-screen-fitting/) | Medium | precompute words fit per start index |
| 467 | [Unique Substrings in Wraparound String](https://leetcode.com/problems/unique-substrings-in-wraparound-string/) | Medium | max run ending at each char, sum maxima |
| 487 | [Max Consecutive Ones II](https://leetcode.com/problems/max-consecutive-ones-ii/) | Medium | dp track ones with one flip |
| 650 | [2 Keys Keyboard](https://leetcode.com/problems/2-keys-keyboard/) | Medium | dp[n]=min ops via factor sum |
| 651 | [4 Keys Keyboard](https://leetcode.com/problems/4-keys-keyboard/) | Medium | dp[i] max keys with copy-paste |
| 678 | [Valid Parenthesis String](https://leetcode.com/problems/valid-parenthesis-string/) | Medium | track min/max open paren range |
| 740 | [Delete and Earn](https://leetcode.com/problems/delete-and-earn/) | Medium | house-robber on value counts |
| 790 | [Domino and Tromino Tiling](https://leetcode.com/problems/domino-and-tromino-tiling/) | Medium | tiling recurrence over columns |
| 838 | [Push Dominoes](https://leetcode.com/problems/push-dominoes/) | Medium | forces from left/right per position |
| 845 | [Longest Mountain in Array](https://leetcode.com/problems/longest-mountain-in-array/) | Medium | up/down run lengths per index |
| 898 | [Bitwise ORs of Subarrays](https://leetcode.com/problems/bitwise-ors-of-subarrays/) | Medium | set of OR values ending at i |
| 926 | [Flip String to Monotone Increasing](https://leetcode.com/problems/flip-string-to-monotone-increasing/) | Medium | track cost of 0-prefix vs 1-suffix |
| 978 | [Longest Turbulent Subarray](https://leetcode.com/problems/longest-turbulent-subarray/) | Medium | dp up/down alternating run lengths |
| 983 | [Minimum Cost For Tickets](https://leetcode.com/problems/minimum-cost-for-tickets/) | Medium | dp[day]=min over 1/7/30-day passes |
| 1024 | [Video Stitching](https://leetcode.com/problems/video-stitching/) | Medium | min clips to cover interval up to T |
| 1043 | [Partition Array for Maximum Sum](https://leetcode.com/problems/partition-array-for-maximum-sum/) | Medium | dp[i] partition last k window |
| 1105 | [Filling Bookcase Shelves](https://leetcode.com/problems/filling-bookcase-shelves/) | Medium | dp[i] place prefix of books on last shelf |
| 1477 | [Find Two Non-overlapping Sub-arrays Each With Target Sum](https://leetcode.com/problems/find-two-non-overlapping-sub-arrays-each-with-target-sum/) | Medium | prefix-sum best subarray left, combine with right |
| 1493 | [Longest Subarray of 1's After Deleting One Element](https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/) | Medium | longest window with one deletion |
| 1567 | [Maximum Length of Subarray With Positive Product](https://leetcode.com/problems/maximum-length-of-subarray-with-positive-product/) | Medium | track pos/neg product run lengths |
| 1578 | [Minimum Time to Make Rope Colorful](https://leetcode.com/problems/minimum-time-to-make-rope-colorful/) | Medium | dp remove dups keep max in run |
| 1653 | [Minimum Deletions to Make String Balanced](https://leetcode.com/problems/minimum-deletions-to-make-string-balanced/) | Medium | track b-count vs delete-a prefix |
| 1696 | [Jump Game VI](https://leetcode.com/problems/jump-game-vi/) | Medium | dp[i]=max window prev + value |
| 1824 | [Minimum Sideway Jumps](https://leetcode.com/problems/minimum-sideway-jumps/) | Medium | dp per lane over positions |
| 1871 | [Jump Game VII](https://leetcode.com/problems/jump-game-vii/) | Medium | reachability dp with sliding window range |
| 1884 | [Egg Drop With 2 Eggs and N Floors](https://leetcode.com/problems/egg-drop-with-2-eggs-and-n-floors/) | Medium | dp over floors with 2 eggs |
| 1888 | [Minimum Number of Flips to Make the Binary String Alternating](https://leetcode.com/problems/minimum-number-of-flips-to-make-the-binary-string-alternating/) | Medium | sliding window flips to alternating |
| 1997 | [First Day Where You Have Been in All the Rooms](https://leetcode.com/problems/first-day-where-you-have-been-in-all-the-rooms/) | Medium | dp[i] first-visit day via nextVisit recurrence |
| 2008 | [Maximum Earnings From Taxi](https://leetcode.com/problems/maximum-earnings-from-taxi/) | Medium | dp[i] skip/take ride ending at i |
| 2052 | [Minimum Cost to Separate Sentence Into Rows](https://leetcode.com/problems/minimum-cost-to-separate-sentence-into-rows/) | Medium | dp[i] min cost to break rows |
| 2054 | [Two Best Non-Overlapping Events](https://leetcode.com/problems/two-best-non-overlapping-events/) | Medium | sort events, best suffix + binary search |
| 2086 | [Minimum Number of Food Buckets to Feed the Hamsters](https://leetcode.com/problems/minimum-number-of-food-buckets-to-feed-the-hamsters/) | Medium | dp place buckets left/right per hamster |
| 2100 | [Find Good Days to Rob the Bank](https://leetcode.com/problems/find-good-days-to-rob-the-bank/) | Medium | prefix non-increasing/non-decreasing runs |
| 2110 | [Number of Smooth Descent Periods of a Stock](https://leetcode.com/problems/number-of-smooth-descent-periods-of-a-stock/) | Medium | count runs, sum k(k+1)/2 |
| 2140 | [Solving Questions With Brainpower](https://leetcode.com/problems/solving-questions-with-brainpower/) | Medium | dp[i]=max(skip, take+dp[i+brain+1]) |
| 2266 | [Count Number of Texts](https://leetcode.com/problems/count-number-of-texts/) | Medium | tribonacci/tetranacci per run of digits |
| 2289 | [Steps to Make Array Non-decreasing](https://leetcode.com/problems/steps-to-make-array-non-decreasing/) | Medium | monotonic stack steps to remove |
| 2297 | [Jump Game VIII](https://leetcode.com/problems/jump-game-viii/) | Medium | dp jump min cost within range |
| 2311 | [Longest Binary Subsequence Less Than or Equal to K](https://leetcode.com/problems/longest-binary-subsequence-less-than-or-equal-to-k/) | Medium | greedy/dp longest subseq value<=k |
| 2320 | [Count Number of Ways to Place Houses](https://leetcode.com/problems/count-number-of-ways-to-place-houses/) | Medium | fib-like no adjacent houses squared |
| 2327 | [Number of People Aware of a Secret](https://leetcode.com/problems/number-of-people-aware-of-a-secret/) | Medium | dp new-knowers per day sliding window |
| 2369 | [Check if There is a Valid Partition For The Array](https://leetcode.com/problems/check-if-there-is-a-valid-partition-for-the-array/) | Medium | dp[i] valid if 2/3 partition ends here |
| 2380 | [Time Needed to Rearrange a Binary String](https://leetcode.com/problems/time-needed-to-rearrange-a-binary-string/) | Medium | dp time to clear each character |
| 2420 | [Find All Good Indices](https://leetcode.com/problems/find-all-good-indices/) | Medium | prefix non-inc / suffix non-dec runs |
| 2436 | [Minimum Split Into Subarrays With GCD Greater Than One](https://leetcode.com/problems/minimum-split-into-subarrays-with-gcd-greater-than-one/) | Medium | dp[i] min splits, running gcd |
| 2464 | [Minimum Subarrays in a Valid Split](https://leetcode.com/problems/minimum-subarrays-in-a-valid-split/) | Medium | dp[i] min splits via gcd prefix |
| 2522 | [Partition String Into Substrings With Values at Most K](https://leetcode.com/problems/partition-string-into-substrings-with-values-at-most-k/) | Medium | dp[i] partitions, value<=k substrings |
| 2560 | [House Robber IV](https://leetcode.com/problems/house-robber-iv/) | Medium | binary search cap + house-robber feasibility |
| 2571 | [Minimum Operations to Reduce an Integer to](https://leetcode.com/problems/minimum-operations-to-reduce-an-integer-to-0/) | Medium | dp on bits add/subtract powers of two |
| 2616 | [Minimize the Maximum Difference of Pairs](https://leetcode.com/problems/minimize-the-maximum-difference-of-pairs/) | Medium | binary search + greedy pairing dp |
| 2645 | [Minimum Additions to Make Valid String](https://leetcode.com/problems/minimum-additions-to-make-valid-string/) | Medium | dp[i] insertions to match abc cycle |
| 2707 | [Extra Characters in a String](https://leetcode.com/problems/extra-characters-in-a-string/) | Medium | dp[i] min extras, dictionary cut |
| 2712 | [Minimum Cost to Make All Characters Equal](https://leetcode.com/problems/minimum-cost-to-make-all-characters-equal/) | Medium | dp prefix/suffix flip costs |
| 2746 | [Decremental String Concatenation](https://leetcode.com/problems/decremental-string-concatenation/) | Medium | dp[i][endchar] min length concatenating |
| 2767 | [Partition String Into Minimum Beautiful Substrings](https://leetcode.com/problems/partition-string-into-minimum-beautiful-substrings/) | Medium | partition dp[i] min beautiful substrings |
| 2770 | [Maximum Number of Jumps to Reach the Last Index](https://leetcode.com/problems/maximum-number-of-jumps-to-reach-the-last-index/) | Medium | dp[i]=1+max dp[j] within jump range |
| 2771 | [Longest Non-decreasing Subarray From Two Arrays](https://leetcode.com/problems/longest-non-decreasing-subarray-from-two-arrays/) | Medium | dp[i][0/1] longest nondecreasing pick |
| 2786 | [Visit Array Positions to Maximize Score](https://leetcode.com/problems/visit-array-positions-to-maximize-score/) | Medium | dp per parity of position value |
| 2811 | [Check if it is Possible to Split Array](https://leetcode.com/problems/check-if-it-is-possible-to-split-array/) | Medium | interval dp / greedy valid split |
| 2830 | [Maximize the Profit as the Salesman](https://leetcode.com/problems/maximize-the-profit-as-the-salesman/) | Medium | sort offers, dp take/skip max gold |
| 2892 | [Minimizing Array After Replacing Pairs With Their Product](https://leetcode.com/problems/minimizing-array-after-replacing-pairs-with-their-product/) | Medium | dp minimize array via product merges |
| 2901 | [Longest Unequal Adjacent Groups Subsequence II](https://leetcode.com/problems/longest-unequal-adjacent-groups-subsequence-ii/) | Medium | dp[i] longest chain hamming-dist-1 adjacent groups |
| 2919 | [Minimum Increment Operations to Make Array Beautiful](https://leetcode.com/problems/minimum-increment-operations-to-make-array-beautiful/) | Medium | dp with window of last three |
| 2944 | [Minimum Number of Coins for Fruits](https://leetcode.com/problems/minimum-number-of-coins-for-fruits/) | Medium | dp min cost with free-fruit range |
| 2957 | [Remove Adjacent Almost-Equal Characters](https://leetcode.com/problems/remove-adjacent-almost-equal-characters/) | Medium | greedy/dp removals of near-equal adjacent chars |
| 3144 | [Minimum Substring Partition of Equal Character Frequency](https://leetcode.com/problems/minimum-substring-partition-of-equal-character-frequency/) | Medium | dp[i] min partitions with balanced char frequency |
| 3147 | [Taking Maximum Energy From the Mystic Dungeon](https://leetcode.com/problems/taking-maximum-energy-from-the-mystic-dungeon/) | Medium | suffix dp jumping by k, max energy |
| 3176 | [Find the Maximum Length of a Good Subsequence I](https://leetcode.com/problems/find-the-maximum-length-of-a-good-subsequence-i/) | Medium | dp[val][k] longest good subsequence |
| 3186 | [Maximum Total Damage With Spell Casting](https://leetcode.com/problems/maximum-total-damage-with-spell-casting/) | Medium | house-robber on damage values skip ±1,±2 |
| 3192 | [Minimum Operations to Make Binary Array Elements Equal to One II](https://leetcode.com/problems/minimum-operations-to-make-binary-array-elements-equal-to-one-ii/) | Medium | greedy prefix flips count to make all ones |
| 3196 | [Maximize Total Cost of Alternating Subarrays](https://leetcode.com/problems/maximize-total-cost-of-alternating-subarrays/) | Medium | dp[i] with sign-alternation state |
| 3201 | [Find the Maximum Length of Valid Subsequence I](https://leetcode.com/problems/find-the-maximum-length-of-valid-subsequence-i/) | Medium | dp on parity pattern subsequence |
| 3202 | [Find the Maximum Length of Valid Subsequence II](https://leetcode.com/problems/find-the-maximum-length-of-valid-subsequence-ii/) | Medium | dp[mod][last%k] longest equal-sum-mod subseq |
| 3205 | [Maximum Array Hopping Score I](https://leetcode.com/problems/maximum-array-hopping-score-i/) | Medium | dp over hop targets max score |
| 3284 | [Sum of Consecutive Subarrays](https://leetcode.com/problems/sum-of-consecutive-subarrays/) | Medium | dp count consecutive subarrays sum |
| 3290 | [Maximum Multiplication Score](https://leetcode.com/problems/maximum-multiplication-score/) | Medium | dp choosing consecutive products max score |
| 3291 | [Minimum Number of Valid Strings to Form Target I](https://leetcode.com/problems/minimum-number-of-valid-strings-to-form-target-i/) | Medium | dp[i] min pieces, prefix-set reachable extensions |
| 3429 | [Paint House IV](https://leetcode.com/problems/paint-house-iv/) | Medium | dp[i][color1][color2] paint houses two sides |
| 3434 | [Maximum Frequency After Subarray Operation](https://leetcode.com/problems/maximum-frequency-after-subarray-operation/) | Medium | dp tracking value-change run |
| 3458 | [Select K Disjoint Special Substrings](https://leetcode.com/problems/select-k-disjoint-special-substrings/) | Medium | dp[i] pick k disjoint special substrings |
| 3473 | [Sum of K Subarrays With Length at Least M](https://leetcode.com/problems/sum-of-k-subarrays-with-length-at-least-m/) | Medium | dp[i][k] best k subarrays min-length M |
| 3557 | [Find Maximum Number of Non Intersecting Substrings](https://leetcode.com/problems/find-maximum-number-of-non-intersecting-substrings/) | Medium | dp weighted-interval max non-overlapping substrings |
| 3599 | [Partition Array to Minimize XOR](https://leetcode.com/problems/partition-array-to-minimize-xor/) | Medium | dp[i][k] partition min XOR prefix |
| 3628 | [Maximum Number of Subsequences After One Inserting](https://leetcode.com/problems/maximum-number-of-subsequences-after-one-inserting/) | Medium | count 'lct' subsequences after one insert |
| 3638 | [Maximum Balanced Shipments](https://leetcode.com/problems/maximum-balanced-shipments/) | Medium | greedy/dp count balanced shipment cuts |
| 3654 | [Minimum Sum After Divisible Sum Deletions](https://leetcode.com/problems/minimum-sum-after-divisible-sum-deletions/) | Medium | dp with prefix-sum divisible deletions |
| 3660 | [Jump Game IX](https://leetcode.com/problems/jump-game-ix/) | Medium | dp reachable index jump rules |
| 3693 | [Climbing Stairs II](https://leetcode.com/problems/climbing-stairs-ii/) | Medium | matrix-expo generalized climbing stairs |
| 3717 | [Minimum Operations to Make the Array Beautiful](https://leetcode.com/problems/minimum-operations-to-make-the-array-beautiful/) | Medium | dp over adjustment operations |
| 3738 | [Longest Non-Decreasing Subarray After Replacing at Most One Element](https://leetcode.com/problems/longest-non-decreasing-subarray-after-replacing-at-most-one-element/) | Medium | dp non-decreasing run with one replace |
| 3840 | [House Robber V](https://leetcode.com/problems/house-robber-v/) | Medium | house robber variant dp on line |
| 3891 | [Minimum Increase to Maximize Special Indices](https://leetcode.com/problems/minimum-increase-to-maximize-special-indices/) | Medium | dp increments to maximize special indices |
| 3952 | [Maximum Total Value of Covered Indices](https://leetcode.com/problems/maximum-total-value-of-covered-indices/) | Medium | dp over covered index intervals max value |
| 3965 | [Finish Time of Tasks I](https://leetcode.com/problems/finish-time-of-tasks-i/) | Medium | sequential task finish-time simulation dp |
| 3980 | [Minimum Operations to Transform Binary String](https://leetcode.com/problems/minimum-operations-to-transform-binary-string/) | Medium | dp over transitions of binary string ops |
| 32 | [Longest Valid Parentheses](https://leetcode.com/problems/longest-valid-parentheses/) | Hard | dp[i] valid parens ending at i |
| 140 | [Word Break II](https://leetcode.com/problems/word-break-ii/) | Hard | dp[i] word-break with memoized sentence build |
| 265 | [Paint House II](https://leetcode.com/problems/paint-house-ii/) | Hard | dp[i][c] min excluding same color, track two mins |
| 403 | [Frog Jump](https://leetcode.com/problems/frog-jump/) | Hard | dp[stone]=set of reachable jump sizes |
| 472 | [Concatenated Words](https://leetcode.com/problems/concatenated-words/) | Hard | word-break dp over string index |
| 552 | [Student Attendance Record II](https://leetcode.com/problems/student-attendance-record-ii/) | Hard | state machine on absent/late counts |
| 639 | [Decode Ways II](https://leetcode.com/problems/decode-ways-ii/) | Hard | decode ways dp[i] with wildcard |
| 656 | [Coin Path](https://leetcode.com/problems/coin-path/) | Hard | dp[i] min cost jump within B, lexicographic path |
| 689 | [Maximum Sum of 3 Non-Overlapping Subarrays](https://leetcode.com/problems/maximum-sum-of-3-non-overlapping-subarrays/) | Hard | prefix sums + best-left/best-right windows |
| 801 | [Minimum Swaps To Make Sequences Increasing](https://leetcode.com/problems/minimum-swaps-to-make-sequences-increasing/) | Hard | dp[i][swap/noswap] keep both increasing |
| 818 | [Race Car](https://leetcode.com/problems/race-car/) | Hard | dp[target] BFS/DP over speed-position states |
| 828 | [Count Unique Characters of All Substrings of a Given String](https://leetcode.com/problems/count-unique-characters-of-all-substrings-of-a-given-string/) | Hard | per-char contribution via prev two positions |
| 975 | [Odd Even Jump](https://leetcode.com/problems/odd-even-jump/) | Hard | dp odd/even jumps via next-greater |
| 1187 | [Make Array Strictly Increasing](https://leetcode.com/problems/make-array-strictly-increasing/) | Hard | dp[i][val] min swaps keeping increasing |
| 1220 | [Count Vowels Permutation](https://leetcode.com/problems/count-vowels-permutation/) | Hard | count per last-vowel state transitions |
| 1235 | [Maximum Profit in Job Scheduling](https://leetcode.com/problems/maximum-profit-in-job-scheduling/) | Hard | sort by end, dp + binary search |
| 1278 | [Palindrome Partitioning III](https://leetcode.com/problems/palindrome-partitioning-iii/) | Hard | partition into k palindromes min changes |
| 1320 | [Minimum Distance to Type a Word Using Two Fingers](https://leetcode.com/problems/minimum-distance-to-type-a-word-using-two-fingers/) | Hard | dp[i][other finger] min distance |
| 1326 | [Minimum Number of Taps to Open to Water a Garden](https://leetcode.com/problems/minimum-number-of-taps-to-open-to-water-a-garden/) | Hard | interval-to-reach dp / greedy jump |
| 1340 | [Jump Game V](https://leetcode.com/problems/jump-game-v/) | Hard | dp[i] max reach jumping within d, memo |
| 1388 | [Pizza With 3n Slices](https://leetcode.com/problems/pizza-with-3n-slices/) | Hard | circular house-robber pick n/3 non-adjacent |
| 1402 | [Reducing Dishes](https://leetcode.com/problems/reducing-dishes/) | Hard | sort desc, take-or-skip suffix sums |
| 1416 | [Restore The Array](https://leetcode.com/problems/restore-the-array/) | Hard | dp[i]=sum over valid last-number splits |
| 1425 | [Constrained Subsequence Sum](https://leetcode.com/problems/constrained-subsequence-sum/) | Hard | dp[i]=nums[i]+max window dp, deque |
| 1526 | [Minimum Number of Increments on Subarrays to Form a Target Array](https://leetcode.com/problems/minimum-number-of-increments-on-subarrays-to-form-a-target-array/) | Hard | sum increments where target[i]>target[i-1] |
| 1531 | [String Compression II](https://leetcode.com/problems/string-compression-ii/) | Hard | dp[i][k] deletions with run-length cost |
| 1537 | [Get the Maximum Score](https://leetcode.com/problems/get-the-maximum-score/) | Hard | two-pointer merge max path sums |
| 1687 | [Delivering Boxes from Storage to Ports](https://leetcode.com/problems/delivering-boxes-from-storage-to-ports/) | Hard | dp over boxes + monotonic deque window |
| 1883 | [Minimum Skips to Arrive at Meeting On Time](https://leetcode.com/problems/minimum-skips-to-arrive-at-meeting-on-time/) | Hard | dp[i][skips] min arrival time |
| 2163 | [Minimum Difference in Sums After Removal of Elements](https://leetcode.com/problems/minimum-difference-in-sums-after-removal-of-elements/) | Hard | prefix min-sum, suffix max-sum with heaps |
| 2167 | [Minimum Time to Remove All Cars Containing Illegal Goods](https://leetcode.com/problems/minimum-time-to-remove-all-cars-containing-illegal-goods/) | Hard | prefix/suffix min removal costs |
| 2209 | [Minimum White Tiles After Covering With Carpets](https://leetcode.com/problems/minimum-white-tiles-after-covering-with-carpets/) | Hard | dp[i][carpets] cover or skip white tile |
| 2263 | [Make Array Non-decreasing or Non-increasing](https://leetcode.com/problems/make-array-non-decreasing-or-non-increasing/) | Hard | dp[i][value] min cost monotone |
| 2355 | [Maximum Number of Books You Can Take](https://leetcode.com/problems/maximum-number-of-books-you-can-take/) | Hard | monotonic stack, valid staircase sums |
| 2478 | [Number of Beautiful Partitions](https://leetcode.com/problems/number-of-beautiful-partitions/) | Hard | partition into k beautiful segments dp[i][k] |
| 2547 | [Minimum Cost to Split an Array](https://leetcode.com/problems/minimum-cost-to-split-an-array/) | Hard | dp[i] partition cost with importance |
| 2945 | [Find Maximum Non-decreasing Array Length](https://leetcode.com/problems/find-maximum-non-decreasing-array-length/) | Hard | dp max segments non-decreasing sums |
| 2969 | [Minimum Number of Coins for Fruits II](https://leetcode.com/problems/minimum-number-of-coins-for-fruits-ii/) | Hard | dp min cost + monotonic deque window |
| 3003 | [Maximize the Number of Partitions After Operations](https://leetcode.com/problems/maximize-the-number-of-partitions-after-operations/) | Hard | dp partition min-cut with one change, distinct chars |
| 3077 | [Maximum Strength of K Disjoint Subarrays](https://leetcode.com/problems/maximum-strength-of-k-disjoint-subarrays/) | Hard | dp[i][k][sign] alternating k-subarray sums |
| 3165 | [Maximum Sum of Subsequence With Non-adjacent Elements](https://leetcode.com/problems/maximum-sum-of-subsequence-with-non-adjacent-elements/) | Hard | non-adjacent max sum with updates |
| 3213 | [Construct String with Minimum Cost](https://leetcode.com/problems/construct-string-with-minimum-cost/) | Hard | dp[i]=min cost using word matches |
| 3229 | [Minimum Operations to Make Array Equal to Target](https://leetcode.com/problems/minimum-operations-to-make-array-equal-to-target/) | Hard | operations from diff array sign changes |
| 3292 | [Minimum Number of Valid Strings to Form Target II](https://leetcode.com/problems/minimum-number-of-valid-strings-to-form-target-ii/) | Hard | min pieces cover target, Aho/Z + dp |
| 3351 | [Sum of Good Subsequences](https://leetcode.com/problems/sum-of-good-subsequences/) | Hard | dp track sum and count by last value |
| 3414 | [Maximum Score of Non-overlapping Intervals](https://leetcode.com/problems/maximum-score-of-non-overlapping-intervals/) | Hard | sort intervals, weighted job scheduling dp |
| 3505 | [Minimum Operations to Make Elements Within K Subarrays Equal](https://leetcode.com/problems/minimum-operations-to-make-elements-within-k-subarrays-equal/) | Hard | dp partition into k subarrays min cost, sliding median |
| 3640 | [Trionic Array II](https://leetcode.com/problems/trionic-array-ii/) | Hard | dp segment up-down-up subarray |
| 3830 | [Longest Alternating Subarray After Removing At Most One Element](https://leetcode.com/problems/longest-alternating-subarray-after-removing-at-most-one-element/) | Hard | dp alternating run with at most one deletion |
| 3892 | [Minimum Operations to Achieve At Least K Peaks](https://leetcode.com/problems/minimum-operations-to-achieve-at-least-k-peaks/) | Hard | dp peaks count with k operations |
| 3915 | [Maximum Sum of Alternating Subsequence With Distance at Least K](https://leetcode.com/problems/maximum-sum-of-alternating-subsequence-with-distance-at-least-k/) | Hard | dp alternating pick with distance gap |
| 3956 | [Maximum Sum of M Non-Overlapping Subarrays I](https://leetcode.com/problems/maximum-sum-of-m-non-overlapping-subarrays-i/) | Hard | dp[i][j] max m non-overlap subarrays |
| 3957 | [Maximum Sum of M Non-Overlapping Subarrays II](https://leetcode.com/problems/maximum-sum-of-m-non-overlapping-subarrays-ii/) | Hard | dp[i][j] m non-overlapping subarrays |
| 3967 | [Finish Time of Tasks II](https://leetcode.com/problems/finish-time-of-tasks-ii/) | Hard | dp scheduling finish times |
| 4023 | [Elevator Requests II](https://leetcode.com/problems/elevator-requests-ii/) | Hard | dp over sorted requests, elevator batching |
| 4027 | [Elevator Requests III](https://leetcode.com/problems/elevator-requests-iii/) | Hard | dp over elevator request states |

---

## Grid / Matrix Path DP (2D)

**53 problems.** State is a cell `(i,j)`; you accumulate a cost/count while moving through a grid (down/right, or all 4 directions with memoization).

- **Recognize it when:** Problem lives on a 2D board: paths, min/max path sum, squares of 1s, falling paths, obstacle grids.
- **Recurrence:** `dp[i][j] = grid[i][j] + best(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`
- **Complexity:** Time `O(m·n)`, space `O(m·n)` often reducible to `O(n)` (one row).

| # | Problem | Difficulty | Core idea |
|---|---------|:----------:|-----------|
| 62 | [Unique Paths](https://leetcode.com/problems/unique-paths/) | Medium | dp[i][j]=dp[i-1][j]+dp[i][j-1] |
| 63 | [Unique Paths II](https://leetcode.com/problems/unique-paths-ii/) | Medium | dp[i][j] paths sum, skip obstacles |
| 64 | [Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/) | Medium | dp[i][j]=grid+min(up,left) |
| 120 | [Triangle](https://leetcode.com/problems/triangle/) | Medium | dp[i][j]=val+min(dp below adjacent) |
| 221 | [Maximal Square](https://leetcode.com/problems/maximal-square/) | Medium | dp[i][j]=min(top,left,diag)+1 square side |
| 361 | [Bomb Enemy](https://leetcode.com/problems/bomb-enemy/) | Medium | row/col enemy-kill prefix counts on grid |
| 542 | [01 Matrix](https://leetcode.com/problems/01-matrix/) | Medium | two-pass min distance BFS/dp |
| 562 | [Longest Line of Consecutive One in Matrix](https://leetcode.com/problems/longest-line-of-consecutive-one-in-matrix/) | Medium | dp per cell 4 directions consecutive |
| 576 | [Out of Boundary Paths](https://leetcode.com/problems/out-of-boundary-paths/) | Medium | dp[i][j][moves] paths off boundary |
| 764 | [Largest Plus Sign](https://leetcode.com/problems/largest-plus-sign/) | Medium | 4-direction arm lengths min per cell |
| 931 | [Minimum Falling Path Sum](https://leetcode.com/problems/minimum-falling-path-sum/) | Medium | dp row from min of three above |
| 1139 | [Largest 1-Bordered Square](https://leetcode.com/problems/largest-1-bordered-square/) | Medium | prefix runs of 1s, check borders |
| 1162 | [As Far from Land as Possible](https://leetcode.com/problems/as-far-from-land-as-possible/) | Medium | BFS/DP distance from land cells |
| 1277 | [Count Square Submatrices with All Ones](https://leetcode.com/problems/count-square-submatrices-with-all-ones/) | Medium | dp[i][j]=1+min neighbors square size |
| 1504 | [Count Submatrices With All Ones](https://leetcode.com/problems/count-submatrices-with-all-ones/) | Medium | count all-one submatrices via heights |
| 1594 | [Maximum Non Negative Product in a Matrix](https://leetcode.com/problems/maximum-non-negative-product-in-a-matrix/) | Medium | track max/min product path per cell |
| 1937 | [Maximum Number of Points with Cost](https://leetcode.com/problems/maximum-number-of-points-with-cost/) | Medium | row dp with left/right running max |
| 2304 | [Minimum Path Cost in a Grid](https://leetcode.com/problems/minimum-path-cost-in-a-grid/) | Medium | dp[i][j]=cell+min(next+move cost) |
| 2510 | [Check if There is a Path With Equal Number of 0's And 1's](https://leetcode.com/problems/check-if-there-is-a-path-with-equal-number-of-0s-and-1s/) | Medium | grid path with balance state |
| 2556 | [Disconnect Path in a Binary Matrix by at Most One Flip](https://leetcode.com/problems/disconnect-path-in-a-binary-matrix-by-at-most-one-flip/) | Medium | count grid paths, flip disconnects if unique path |
| 2684 | [Maximum Number of Moves in a Grid](https://leetcode.com/problems/maximum-number-of-moves-in-a-grid/) | Medium | dp move right/diagonal to greater cell |
| 3122 | [Minimum Number of Operations to Satisfy Conditions](https://leetcode.com/problems/minimum-number-of-operations-to-satisfy-conditions/) | Medium | dp[col][value] min changes column transitions |
| 3148 | [Maximum Difference Score in a Grid](https://leetcode.com/problems/maximum-difference-score-in-a-grid/) | Medium | dp cell max difference from prefix min |
| 3332 | [Maximum Points Tourist Can Earn](https://leetcode.com/problems/maximum-points-tourist-can-earn/) | Medium | dp[day][city] stay or move |
| 3393 | [Count Paths With the Given XOR Value](https://leetcode.com/problems/count-paths-with-the-given-xor-value/) | Medium | dp[i][j][xor] path xor counts |
| 3418 | [Maximum Amount of Money Robot Can Earn](https://leetcode.com/problems/maximum-amount-of-money-robot-can-earn/) | Medium | path dp with skip-two-cells state |
| 3466 | [Maximum Coin Collection](https://leetcode.com/problems/maximum-coin-collection/) | Medium | dp two-lane path max coins |
| 3603 | [Minimum Cost Path with Alternating Directions II](https://leetcode.com/problems/minimum-cost-path-with-alternating-directions-ii/) | Medium | dp[i][j][dir] min cost alternating-direction grid |
| 3665 | [Twisted Mirror Path Count](https://leetcode.com/problems/twisted-mirror-path-count/) | Medium | grid path count with mirror direction state |
| 3742 | [Maximum Path Score in a Grid](https://leetcode.com/problems/maximum-path-score-in-a-grid/) | Medium | dp max path score grid movement |
| 3882 | [Minimum XOR Path in a Grid](https://leetcode.com/problems/minimum-xor-path-in-a-grid/) | Medium | dp min XOR path over grid cells |
| 3938 | [Maximum Path Intersection Sum in a Grid](https://leetcode.com/problems/maximum-path-intersection-sum-in-a-grid/) | Medium | max sum over intersecting grid paths DP |
| 4016 | [Maximum Area of Two Non-Overlapping Square Submatrices](https://leetcode.com/problems/maximum-area-of-two-non-overlapping-square-submatrices/) | Medium | prefix-sum + max square submatrix per cell dp |
| 85 | [Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/) | Hard | histogram heights per row, max rectangle |
| 174 | [Dungeon Game](https://leetcode.com/problems/dungeon-game/) | Hard | min health from bottom-right backward |
| 741 | [Cherry Pickup](https://leetcode.com/problems/cherry-pickup/) | Hard | two paths simultaneously in grid |
| 1289 | [Minimum Falling Path Sum II](https://leetcode.com/problems/minimum-falling-path-sum-ii/) | Hard | falling path, min excluding same col |
| 1301 | [Number of Paths with Max Score](https://leetcode.com/problems/number-of-paths-with-max-score/) | Hard | dp path max score with count |
| 1444 | [Number of Ways of Cutting a Pizza](https://leetcode.com/problems/number-of-ways-of-cutting-a-pizza/) | Hard | dp cuts with 2D prefix apple counts |
| 1463 | [Cherry Pickup II](https://leetcode.com/problems/cherry-pickup-ii/) | Hard | two robots dp over row, cols pair |
| 1473 | [Paint House III](https://leetcode.com/problems/paint-house-iii/) | Hard | dp[house][color][neighborhoods] |
| 2088 | [Count Fertile Pyramids in a Land](https://leetcode.com/problems/count-fertile-pyramids-in-a-land/) | Hard | dp pyramid height from cells below |
| 2267 | [Check if There Is a Valid Parentheses String Path](https://leetcode.com/problems/check-if-there-is-a-valid-parentheses-string-path/) | Hard | dp[cell][balance] valid paren path |
| 2435 | [Paths in Matrix Whose Sum Is Divisible by K](https://leetcode.com/problems/paths-in-matrix-whose-sum-is-divisible-by-k/) | Hard | dp[i][j][r] paths by sum mod k |
| 3018 | [Maximum Number of Removal Queries That Can Be Processed I](https://leetcode.com/problems/maximum-number-of-removal-queries-that-can-be-processed-i/) | Hard | dp remove from grid corners |
| 3225 | [Maximum Score From Grid Operations](https://leetcode.com/problems/maximum-score-from-grid-operations/) | Hard | dp over columns with painted prefix heights |
| 3256 | [Maximum Value Sum by Placing Three Rooks I](https://leetcode.com/problems/maximum-value-sum-by-placing-three-rooks-i/) | Hard | dp over rows choosing non-attacking columns |
| 3257 | [Maximum Value Sum by Placing Three Rooks II](https://leetcode.com/problems/maximum-value-sum-by-placing-three-rooks-ii/) | Hard | top-3 per row/col placement dp |
| 3363 | [Find the Maximum Number of Fruits Collected](https://leetcode.com/problems/find-the-maximum-number-of-fruits-collected/) | Hard | two diagonal path DP collecting fruits |
| 3459 | [Length of Longest V-Shaped Diagonal Segment](https://leetcode.com/problems/length-of-longest-v-shaped-diagonal-segment/) | Hard | dp diagonal segment with one turn |
| 3651 | [Minimum Cost Path with Teleportations](https://leetcode.com/problems/minimum-cost-path-with-teleportations/) | Hard | grid path with teleport state |
| 3797 | [Count Routes to Climb a Rectangular Grid](https://leetcode.com/problems/count-routes-to-climb-a-rectangular-grid/) | Hard | count grid climb routes summing paths |
| 3906 | [Count Good Integers on a Grid Path](https://leetcode.com/problems/count-good-integers-on-a-grid-path/) | Hard | digit-mod dp over grid path counting |

---

## Knapsack / Subset-Sum

**58 problems.** Pick a subset of items to exactly hit / not exceed a capacity, sum, or target. 0/1 (each item once) vs unbounded (reuse) vs counting variants.

- **Recognize it when:** You choose items against a numeric budget: coin change, target sum, partition equal subset, ones-and-zeroes, combination sum.
- **Recurrence:** 0/1: `dp[c] = max(dp[c], dp[c-w]+v)` iterate capacity **descending**. Unbounded: iterate **ascending**.
- **Complexity:** Time `O(n·C)`, space `O(C)` with the 1D rolling trick. Pseudo-polynomial in capacity `C`.

| # | Problem | Difficulty | Core idea |
|---|---------|:----------:|-----------|
| 279 | [Perfect Squares](https://leetcode.com/problems/perfect-squares/) | Medium | dp[n]=min over square coins |
| 322 | [Coin Change](https://leetcode.com/problems/coin-change/) | Medium | dp[amount]=min coins, unbounded knapsack |
| 377 | [Combination Sum IV](https://leetcode.com/problems/combination-sum-iv/) | Medium | dp[t]+=dp[t-num], order matters |
| 416 | [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) | Medium | subset sum to total/2 |
| 474 | [Ones and Zeroes](https://leetcode.com/problems/ones-and-zeroes/) | Medium | 2D knapsack by zeros/ones |
| 494 | [Target Sum](https://leetcode.com/problems/target-sum/) | Medium | subset sum to (S+target)/2 |
| 518 | [Coin Change II](https://leetcode.com/problems/coin-change-ii/) | Medium | unbounded coin combos dp[amount] |
| 638 | [Shopping Offers](https://leetcode.com/problems/shopping-offers/) | Medium | dp over remaining needs, try each offer |
| 1049 | [Last Stone Weight II](https://leetcode.com/problems/last-stone-weight-ii/) | Medium | partition into two near-equal subsets |
| 1155 | [Number of Dice Rolls With Target Sum](https://leetcode.com/problems/number-of-dice-rolls-with-target-sum/) | Medium | dp[dice][sum] count target sum |
| 1262 | [Greatest Sum Divisible by Three](https://leetcode.com/problems/greatest-sum-divisible-by-three/) | Medium | dp[remainder mod 3] max sum |
| 1774 | [Closest Dessert Cost](https://leetcode.com/problems/closest-dessert-cost/) | Medium | subset-sum toppings closest to target |
| 1981 | [Minimize the Difference Between Target and Chosen Elements](https://leetcode.com/problems/minimize-the-difference-between-target-and-chosen-elements/) | Medium | dp set of reachable sums pick one per row |
| 2184 | [Number of Ways to Build Sturdy Brick Wall](https://leetcode.com/problems/number-of-ways-to-build-sturdy-brick-wall/) | Medium | row combos to width, layer stability transitions |
| 2291 | [Maximum Profit From Trading Stocks](https://leetcode.com/problems/maximum-profit-from-trading-stocks/) | Medium | 0/1 knapsack budget vs stock profit |
| 2310 | [Sum of Numbers With Units Digit K](https://leetcode.com/problems/sum-of-numbers-with-units-digit-k/) | Medium | count numbers ending digit k summing |
| 2431 | [Maximize Total Tastiness of Purchased Fruits](https://leetcode.com/problems/maximize-total-tastiness-of-purchased-fruits/) | Medium | knapsack over amount and coupons |
| 2787 | [Ways to Express an Integer as Sum of Powers](https://leetcode.com/problems/ways-to-express-an-integer-as-sum-of-powers/) | Medium | count subsets summing n with powers |
| 2915 | [Length of the Longest Subsequence That Sums to Target](https://leetcode.com/problems/length-of-the-longest-subsequence-that-sums-to-target/) | Medium | dp[sum]=max length hitting target |
| 2979 | [Most Expensive Item That Can Not Be Bought](https://leetcode.com/problems/most-expensive-item-that-can-not-be-bought/) | Medium | coin-reachability, largest non-buyable value |
| 3180 | [Maximum Total Reward Using Operations I](https://leetcode.com/problems/maximum-total-reward-using-operations-i/) | Medium | dp reachable rewards pick if x>current sum |
| 3183 | [The Number of Ways to Make the Sum](https://leetcode.com/problems/the-number-of-ways-to-make-the-sum/) | Medium | coin-change count ways to sum |
| 3366 | [Minimum Array Sum](https://leetcode.com/problems/minimum-array-sum/) | Medium | dp over count of halving operations |
| 3489 | [Zero Array Transformation IV](https://leetcode.com/problems/zero-array-transformation-iv/) | Medium | subset-sum reachable zero per index |
| 3592 | [Inverse Coin Change](https://leetcode.com/problems/inverse-coin-change/) | Medium | coin-change counting inversion |
| 3610 | [Minimum Number of Primes to Sum to Target](https://leetcode.com/problems/minimum-number-of-primes-to-sum-to-target/) | Medium | unbounded knapsack of primes to target |
| 3647 | [Maximum Weight in Two Bags](https://leetcode.com/problems/maximum-weight-in-two-bags/) | Medium | 2D knapsack over two bag capacities |
| 3685 | [Subsequence Sum After Capping Elements](https://leetcode.com/problems/subsequence-sum-after-capping-elements/) | Medium | subset-sum reachable with capped elements |
| 3877 | [Minimum Removals to Achieve Target XOR](https://leetcode.com/problems/minimum-removals-to-achieve-target-xor/) | Medium | subset dp remove to reach target XOR |
| 3946 | [Maximum Number of Items From Sale I](https://leetcode.com/problems/maximum-number-of-items-from-sale-i/) | Medium | dp over budget picking sale items |
| 805 | [Split Array With Same Average](https://leetcode.com/problems/split-array-with-same-average/) | Hard | subset with target avg, size+sum dp |
| 871 | [Minimum Number of Refueling Stops](https://leetcode.com/problems/minimum-number-of-refueling-stops/) | Hard | dp[i]=max distance with i refuels (heap alt) |
| 879 | [Profitable Schemes](https://leetcode.com/problems/profitable-schemes/) | Hard | 2D knapsack members and profit |
| 956 | [Tallest Billboard](https://leetcode.com/problems/tallest-billboard/) | Hard | dp over height-difference between two sides |
| 1363 | [Largest Multiple of Three](https://leetcode.com/problems/largest-multiple-of-three/) | Hard | dp over digit-sum mod 3 remainder |
| 1449 | [Form Largest Integer With Digits That Add up to Target](https://leetcode.com/problems/form-largest-integer-with-digits-that-add-up-to-target/) | Hard | unbounded knapsack target cost, digits |
| 1575 | [Count All Possible Routes](https://leetcode.com/problems/count-all-possible-routes/) | Hard | dp[node][fuel] count routes |
| 1751 | [Maximum Number of Events That Can Be Attended II](https://leetcode.com/problems/maximum-number-of-events-that-can-be-attended-ii/) | Hard | sort events, take/skip + binary search next |
| 1755 | [Closest Subsequence Sum](https://leetcode.com/problems/closest-subsequence-sum/) | Hard | meet-in-middle subset sums closest to goal |
| 1787 | [Make the XOR of All Segments Equal to Zero](https://leetcode.com/problems/make-the-xor-of-all-segments-equal-to-zero/) | Hard | dp columns mod k, group counts |
| 2035 | [Partition Array Into Two Arrays to Minimize Sum Difference](https://leetcode.com/problems/partition-array-into-two-arrays-to-minimize-sum-difference/) | Hard | meet-in-middle subset sums balance |
| 2188 | [Minimum Time to Finish the Race](https://leetcode.com/problems/minimum-time-to-finish-the-race/) | Hard | best time per laps then dp over total |
| 2218 | [Maximum Value of K Coins From Piles](https://leetcode.com/problems/maximum-value-of-k-coins-from-piles/) | Hard | group knapsack over pile prefixes |
| 2463 | [Minimum Total Distance Traveled](https://leetcode.com/problems/minimum-total-distance-traveled/) | Hard | dp assign robots to factories, min distance |
| 2518 | [Number of Great Partitions](https://leetcode.com/problems/number-of-great-partitions/) | Hard | subset-sum counts, subtract bad splits |
| 2585 | [Number of Ways to Earn Points](https://leetcode.com/problems/number-of-ways-to-earn-points/) | Hard | grouped knapsack over target points |
| 2742 | [Painting the Walls](https://leetcode.com/problems/painting-the-walls/) | Hard | knapsack paid vs free wall time |
| 2809 | [Minimum Time to Make Array Sum At Most x](https://leetcode.com/problems/minimum-time-to-make-array-sum-at-most-x/) | Hard | dp select k to zero, ordered by growth |
| 2902 | [Count of Sub-Multisets With Bounded Sum](https://leetcode.com/problems/count-of-sub-multisets-with-bounded-sum/) | Hard | bounded-count subset-sum counting sliding |
| 3098 | [Find the Sum of Subsequence Powers](https://leetcode.com/problems/find-the-sum-of-subsequence-powers/) | Hard | dp over sorted subseq by count+min-gap |
| 3117 | [Minimum Sum of Values by Dividing Array](https://leetcode.com/problems/minimum-sum-of-values-by-dividing-array/) | Hard | dp[i][j] segments with AND value |
| 3181 | [Maximum Total Reward Using Operations II](https://leetcode.com/problems/maximum-total-reward-using-operations-ii/) | Hard | reachable-reward subset dp with bitset |
| 3444 | [Minimum Increments for Target Multiples in an Array](https://leetcode.com/problems/minimum-increments-for-target-multiples-in-an-array/) | Hard | dp over lcm targets subset cover |
| 3509 | [Maximum Product of Subsequences With an Alternating Sum Equal to K](https://leetcode.com/problems/maximum-product-of-subsequences-with-an-alternating-sum-equal-to-k/) | Hard | dp[sum][parity] max product subsequence |
| 3826 | [Minimum Partition Score](https://leetcode.com/problems/minimum-partition-score/) | Hard | dp partition minimize max score |
| 3836 | [Maximum Score Using Exactly K Pairs](https://leetcode.com/problems/maximum-score-using-exactly-k-pairs/) | Hard | dp[i][k] choose k pairs max score |
| 3981 | [Count Distinct Ways to Form Target from Two Strings](https://leetcode.com/problems/count-distinct-ways-to-form-target-from-two-strings/) | Hard | count ways split target across two |
| 4009 | [Minimum Possible Maximum Waiting Time](https://leetcode.com/problems/minimum-possible-maximum-waiting-time/) | Hard | dp minimize max waiting partition |

---

## Longest Increasing Subsequence (LIS)

**24 problems.** Find the longest / best chain under an ordering constraint. `O(n^2)` DP or `O(n log n)` patience-sorting with binary search.

- **Recognize it when:** Subsequence must be strictly increasing / form a divisible or arithmetic chain / nest (Russian doll).
- **Recurrence:** `dp[i] = 1 + max(dp[j] for j<i if a[j]<a[i])`; or maintain `tails[]` + `bisect`.
- **Complexity:** `O(n^2)` naive, `O(n log n)` with binary search on the tails array.

| # | Problem | Difficulty | Core idea |
|---|---------|:----------:|-----------|
| 300 | [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) | Medium | dp[i]=max prior+1 or patience |
| 368 | [Largest Divisible Subset](https://leetcode.com/problems/largest-divisible-subset/) | Medium | sort, LIS on divisibility chain |
| 376 | [Wiggle Subsequence](https://leetcode.com/problems/wiggle-subsequence/) | Medium | up/down alternating run lengths |
| 435 | [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) | Medium | sort intervals, greedy/LIS non-overlap |
| 646 | [Maximum Length of Pair Chain](https://leetcode.com/problems/maximum-length-of-pair-chain/) | Medium | sort by end, greedy chain |
| 673 | [Number of Longest Increasing Subsequence](https://leetcode.com/problems/number-of-longest-increasing-subsequence/) | Medium | LIS lengths plus count arrays |
| 873 | [Length of Longest Fibonacci Subsequence](https://leetcode.com/problems/length-of-longest-fibonacci-subsequence/) | Medium | dp[j][k] fib chain by pairs |
| 1027 | [Longest Arithmetic Subsequence](https://leetcode.com/problems/longest-arithmetic-subsequence/) | Medium | dp[i][diff] arithmetic subseq |
| 1048 | [Longest String Chain](https://leetcode.com/problems/longest-string-chain/) | Medium | sort by length, dp[word]=predecessor+1 chain |
| 1218 | [Longest Arithmetic Subsequence of Given Difference](https://leetcode.com/problems/longest-arithmetic-subsequence-of-given-difference/) | Medium | hashmap dp[v]=dp[v-d]+1 |
| 1395 | [Count Number of Teams](https://leetcode.com/problems/count-number-of-teams/) | Medium | count smaller/larger on each side |
| 1626 | [Best Team With No Conflicts](https://leetcode.com/problems/best-team-with-no-conflicts/) | Medium | sort by age, LIS max-score on scores |
| 2370 | [Longest Ideal Subsequence](https://leetcode.com/problems/longest-ideal-subsequence/) | Medium | dp per char, adjacent diff<=k |
| 2501 | [Longest Square Streak in an Array](https://leetcode.com/problems/longest-square-streak-in-an-array/) | Medium | dp[x]=1+dp[sqrt x] chain via map |
| 2826 | [Sorting Three Groups](https://leetcode.com/problems/sorting-three-groups/) | Medium | min changes to non-decreasing 3-value |
| 3409 | [Longest Subsequence With Decreasing Adjacent Difference](https://leetcode.com/problems/longest-subsequence-with-decreasing-adjacent-difference/) | Medium | dp longest decreasing-adjacent-diff subseq |
| 354 | [Russian Doll Envelopes](https://leetcode.com/problems/russian-doll-envelopes/) | Hard | sort width, LIS on heights |
| 1671 | [Minimum Number of Removals to Make Mountain Array](https://leetcode.com/problems/minimum-number-of-removals-to-make-mountain-array/) | Hard | LIS both directions, mountain peak |
| 1691 | [Maximum Height by Stacking Cuboids](https://leetcode.com/problems/maximum-height-by-stacking-cuboids/) | Hard | sort dims then LIS of cuboids |
| 2407 | [Longest Increasing Subsequence II](https://leetcode.com/problems/longest-increasing-subsequence-ii/) | Hard | LIS with segment-tree range max query |
| 2713 | [Maximum Strictly Increasing Cells in a Matrix](https://leetcode.com/problems/maximum-strictly-increasing-cells-in-a-matrix/) | Hard | dp per cell longest increasing chain by value order |
| 2926 | [Maximum Balanced Subsequence Sum](https://leetcode.com/problems/maximum-balanced-subsequence-sum/) | Hard | max-sum subsequence with i-nums increasing, Fenwick |
| 3041 | [Maximize Consecutive Elements in an Array After Modification](https://leetcode.com/problems/maximize-consecutive-elements-in-an-array-after-modification/) | Hard | dp[v]=longest consecutive chain via +1 |
| 3177 | [Find the Maximum Length of a Good Subsequence II](https://leetcode.com/problems/find-the-maximum-length-of-a-good-subsequence-ii/) | Hard | dp[val][used] good subsequence <=k |

---

## Two-Sequence / String-Edit DP

**29 problems.** State `dp[i][j]` over prefixes of TWO strings/arrays. The alignment family: edit distance, LCS, subsequence counting, regex/wildcard matching.

- **Recognize it when:** Two sequences compared cell-by-cell; transition on match vs insert/delete/replace.
- **Recurrence:** `dp[i][j] = dp[i-1][j-1]+1` on match, else `combine(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])`.
- **Complexity:** Time `O(m·n)`, space `O(m·n)` reducible to `O(min(m,n))`.

| # | Problem | Difficulty | Core idea |
|---|---------|:----------:|-----------|
| 392 | [Is Subsequence](https://leetcode.com/problems/is-subsequence/) | Easy | two-pointer subsequence matching |
| 72 | [Edit Distance](https://leetcode.com/problems/edit-distance/) | Medium | dp[i][j] insert/delete/replace min edits |
| 97 | [Interleaving String](https://leetcode.com/problems/interleaving-string/) | Medium | dp[i][j] over s1,s2 prefixes match s3 |
| 583 | [Delete Operation for Two Strings](https://leetcode.com/problems/delete-operation-for-two-strings/) | Medium | LCS then delete complement |
| 712 | [Minimum ASCII Delete Sum for Two Strings](https://leetcode.com/problems/minimum-ascii-delete-sum-for-two-strings/) | Medium | LCS-like min ASCII delete on two strings |
| 718 | [Maximum Length of Repeated Subarray](https://leetcode.com/problems/maximum-length-of-repeated-subarray/) | Medium | dp[i][j]=match+dp[i-1][j-1] |
| 1035 | [Uncrossed Lines](https://leetcode.com/problems/uncrossed-lines/) | Medium | LCS on two arrays |
| 1062 | [Longest Repeating Substring](https://leetcode.com/problems/longest-repeating-substring/) | Medium | dp[i][j] repeated substring length |
| 1143 | [Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) | Medium | dp[i][j] LCS match/skip recurrence |
| 1638 | [Count Substrings That Differ by One Character](https://leetcode.com/problems/count-substrings-that-differ-by-one-character/) | Medium | dp[i][j] runs differing by exactly one |
| 2896 | [Apply Operations to Make Two Strings Equal](https://leetcode.com/problems/apply-operations-to-make-two-strings-equal/) | Medium | dp align two strings with ops |
| 3135 | [Equalize Strings by Adding or Removing Characters at Ends](https://leetcode.com/problems/equalize-strings-by-adding-or-removing-characters-at-ends/) | Medium | longest common substring edit ends |
| 3302 | [Find the Lexicographically Smallest Valid Sequence](https://leetcode.com/problems/find-the-lexicographically-smallest-valid-sequence/) | Medium | dp match with limited edits greedy |
| 3316 | [Find Maximum Removals From Source String](https://leetcode.com/problems/find-maximum-removals-from-source-string/) | Medium | dp[i][j] over source and pattern with removals |
| 3503 | [Longest Palindrome After Substring Concatenation I](https://leetcode.com/problems/longest-palindrome-after-substring-concatenation-i/) | Medium | LCS-like across concatenation with palindrome |
| 10 | [Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/) | Hard | dp[i][j] over string and pattern with * / . |
| 44 | [Wildcard Matching](https://leetcode.com/problems/wildcard-matching/) | Hard | dp[i][j] over string vs pattern with * matching |
| 115 | [Distinct Subsequences](https://leetcode.com/problems/distinct-subsequences/) | Hard | dp[i][j] match subsequence counts |
| 727 | [Minimum Window Subsequence](https://leetcode.com/problems/minimum-window-subsequence/) | Hard | dp[i][j] subsequence match window |
| 960 | [Delete Columns to Make Sorted III](https://leetcode.com/problems/delete-columns-to-make-sorted-iii/) | Hard | LIS over kept columns per position |
| 1092 | [Shortest Common Supersequence](https://leetcode.com/problems/shortest-common-supersequence/) | Hard | LCS then interleave uncovered chars |
| 1458 | [Max Dot Product of Two Subsequences](https://leetcode.com/problems/max-dot-product-of-two-subsequences/) | Hard | dp[i][j] max dot product of subsequences |
| 1639 | [Number of Ways to Form a Target String Given a Dictionary](https://leetcode.com/problems/number-of-ways-to-form-a-target-string-given-a-dictionary/) | Hard | dp[i][j] match target via columns |
| 2060 | [Check if an Original String Exists Given Two Encoded Strings](https://leetcode.com/problems/check-if-an-original-string-exists-given-two-encoded-strings/) | Hard | dp[i][j][diff] over two encoded strings |
| 2430 | [Maximum Deletions on a String](https://leetcode.com/problems/maximum-deletions-on-a-string/) | Hard | LCP dp then dp[i]=1+min matching prefix |
| 2977 | [Minimum Cost to Convert String II](https://leetcode.com/problems/minimum-cost-to-convert-string-ii/) | Hard | dp over index min convert cost |
| 3269 | [Constructing Two Increasing Arrays](https://leetcode.com/problems/constructing-two-increasing-arrays/) | Hard | dp[i][j] cost building two increasing |
| 3504 | [Longest Palindrome After Substring Concatenation II](https://leetcode.com/problems/longest-palindrome-after-substring-concatenation-ii/) | Hard | dp match/palindrome across two strings |
| 3579 | [Minimum Steps to Convert String with Operations](https://leetcode.com/problems/minimum-steps-to-convert-string-with-operations/) | Hard | dp over string transform operations |

---

## Palindrome DP

**18 problems.** Substrings/subsequences that read the same both ways. Interval-flavored: expand around centers or `dp[i][j]` on ranges.

- **Recognize it when:** Palindromic substring/subsequence count, longest, min cuts to partition.
- **Recurrence:** `dp[i][j] = (s[i]==s[j]) && dp[i+1][j-1]`; longest-pal-subseq `dp[i][j]=dp[i+1][j-1]+2` on match.
- **Complexity:** Time `O(n^2)`, space `O(n^2)`.

| # | Problem | Difficulty | Core idea |
|---|---------|:----------:|-----------|
| 5 | [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) | Medium | dp[i][j] expand palindrome ranges |
| 131 | [Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/) | Medium | partition into palindromic substrings |
| 516 | [Longest Palindromic Subsequence](https://leetcode.com/problems/longest-palindromic-subsequence/) | Medium | dp[i][j] LPS extend interval ends |
| 647 | [Palindromic Substrings](https://leetcode.com/problems/palindromic-substrings/) | Medium | expand/dp[i][j] palindrome count |
| 1682 | [Longest Palindromic Subsequence II](https://leetcode.com/problems/longest-palindromic-subsequence-ii/) | Medium | dp[i][j][last] LPS with no two adjacent equal |
| 2002 | [Maximum Product of the Length of Two Palindromic Subsequences](https://leetcode.com/problems/maximum-product-of-the-length-of-two-palindromic-subsequences/) | Medium | max product two disjoint palindromic subseqs |
| 3472 | [Longest Palindromic Subsequence After at Most K Operations](https://leetcode.com/problems/longest-palindromic-subsequence-after-at-most-k-operations/) | Medium | dp[i][j][k] LPS with k mismatch fixes |
| 3844 | [Longest Almost-Palindromic Substring](https://leetcode.com/problems/longest-almost-palindromic-substring/) | Medium | expand centers almost-palindrome substring |
| 132 | [Palindrome Partitioning II](https://leetcode.com/problems/palindrome-partitioning-ii/) | Hard | dp[i] min cuts, extend palindrome partitions |
| 730 | [Count Different Palindromic Subsequences](https://leetcode.com/problems/count-different-palindromic-subsequences/) | Hard | dp[i][j] count distinct palindromic subsequences |
| 1147 | [Longest Chunked Palindrome Decomposition](https://leetcode.com/problems/longest-chunked-palindrome-decomposition/) | Hard | greedy/dp matching prefix-suffix chunks |
| 1216 | [Valid Palindrome III](https://leetcode.com/problems/valid-palindrome-iii/) | Hard | n minus longest palindromic subsequence |
| 1312 | [Minimum Insertion Steps to Make a String Palindrome](https://leetcode.com/problems/minimum-insertion-steps-to-make-a-string-palindrome/) | Hard | n - LPS via LCS with reverse |
| 1745 | [Palindrome Partitioning IV](https://leetcode.com/problems/palindrome-partitioning-iv/) | Hard | palindrome table then split into three |
| 1771 | [Maximize Palindrome Length From Subsequences](https://leetcode.com/problems/maximize-palindrome-length-from-subsequences/) | Hard | longest palindromic subseq over concatenation |
| 2472 | [Maximum Number of Non-overlapping Palindrome Substrings](https://leetcode.com/problems/maximum-number-of-non-overlapping-palindrome-substrings/) | Hard | dp[i] max non-overlap palindrome substrings |
| 2484 | [Count Palindromic Subsequences](https://leetcode.com/problems/count-palindromic-subsequences/) | Hard | dp count length-5 palindromic subsequences |
| 2911 | [Minimum Changes to Make K Semi-palindromes](https://leetcode.com/problems/minimum-changes-to-make-k-semi-palindromes/) | Hard | substring semi-palindrome cost then partition dp |

---

## Interval / Range DP

**39 problems.** State `dp[i][j]` over a contiguous range, transition by choosing a split/last-operation point `k` inside. Matrix-chain family.

- **Recognize it when:** Answer for `[i,j]` builds from smaller inner ranges: burst balloons, merge stones, MCM, remove boxes, min-cost triangulation.
- **Recurrence:** `dp[i][j] = min/max over k in (i,j) of dp[i][k] + dp[k][j] + cost(i,k,j)`
- **Complexity:** Time typically `O(n^3)` (three nested loops: length, left, split), space `O(n^2)`.

| # | Problem | Difficulty | Core idea |
|---|---------|:----------:|-----------|
| 241 | [Different Ways to Add Parentheses](https://leetcode.com/problems/different-ways-to-add-parentheses/) | Medium | split at each operator, combine subresults |
| 375 | [Guess Number Higher or Lower II](https://leetcode.com/problems/guess-number-higher-or-lower-ii/) | Medium | dp[i][j]=min over k of k+max(left,right) |
| 553 | [Optimal Division](https://leetcode.com/problems/optimal-division/) | Medium | maximize/minimize expression parenthesization |
| 813 | [Largest Sum of Averages](https://leetcode.com/problems/largest-sum-of-averages/) | Medium | partition into k groups max avg sum |
| 1039 | [Minimum Score Triangulation of Polygon](https://leetcode.com/problems/minimum-score-triangulation-of-polygon/) | Medium | dp[i][j]=min over split k of triangulation |
| 1130 | [Minimum Cost Tree From Leaf Values](https://leetcode.com/problems/minimum-cost-tree-from-leaf-values/) | Medium | dp[i][j] split, cost=max*max product |
| 1959 | [Minimum Total Space Wasted With K Resizing Operations](https://leetcode.com/problems/minimum-total-space-wasted-with-k-resizing-operations/) | Medium | dp[i][k] split segments min waste |
| 3040 | [Maximum Number of Operations With the Same Score II](https://leetcode.com/problems/maximum-number-of-operations-with-the-same-score-ii/) | Medium | dp[i][j] over shrinking ends by score |
| 3218 | [Minimum Cost for Cutting Cake I](https://leetcode.com/problems/minimum-cost-for-cutting-cake-i/) | Medium | dp[i][j] cut cost splits (greedy) |
| 3469 | [Find Minimum Cost to Remove Array Elements](https://leetcode.com/problems/find-minimum-cost-to-remove-array-elements/) | Medium | dp[i][j] min cost remove pairs from array range |
| 3857 | [Minimum Cost to Split into Ones](https://leetcode.com/problems/minimum-cost-to-split-into-ones/) | Medium | dp[i][j] split range into ones min cost |
| 87 | [Scramble String](https://leetcode.com/problems/scramble-string/) | Hard | dp over substring splits with swap |
| 312 | [Burst Balloons](https://leetcode.com/problems/burst-balloons/) | Hard | dp[i][j] over split balloon k |
| 471 | [Encode String with Shortest Length](https://leetcode.com/problems/encode-string-with-shortest-length/) | Hard | dp[i][j] best encoding over substring split |
| 488 | [Zuma Game](https://leetcode.com/problems/zuma-game/) | Hard | memoized board+hand state expansion |
| 514 | [Freedom Trail](https://leetcode.com/problems/freedom-trail/) | Hard | dp[pos][ring index] min rotations |
| 546 | [Remove Boxes](https://leetcode.com/problems/remove-boxes/) | Hard | dp[i][j][k] range with equal-color count |
| 664 | [Strange Printer](https://leetcode.com/problems/strange-printer/) | Hard | dp[i][j] over range, split point |
| 887 | [Super Egg Drop](https://leetcode.com/problems/super-egg-drop/) | Hard | dp[eggs][moves] eggs drop threshold DP |
| 1000 | [Minimum Cost to Merge Stones](https://leetcode.com/problems/minimum-cost-to-merge-stones/) | Hard | dp[i][j][k] merge with split point |
| 1246 | [Palindrome Removal](https://leetcode.com/problems/palindrome-removal/) | Hard | dp[i][j] remove palindromic subarray |
| 1259 | [Handshakes That Don't Cross](https://leetcode.com/problems/handshakes-that-dont-cross/) | Hard | dp[n]=sum dp[k]*dp[n-2-k] pairing |
| 1335 | [Minimum Difficulty of a Job Schedule](https://leetcode.com/problems/minimum-difficulty-of-a-job-schedule/) | Hard | dp[i][d] partition into d days, max per segment |
| 1478 | [Allocate Mailboxes](https://leetcode.com/problems/allocate-mailboxes/) | Hard | partition houses into k groups min dist |
| 1547 | [Minimum Cost to Cut a Stick](https://leetcode.com/problems/minimum-cost-to-cut-a-stick/) | Hard | dp[i][j] cost over cut positions, split point k |
| 1563 | [Stone Game V](https://leetcode.com/problems/stone-game-v/) | Hard | dp[i][j] split range max score |
| 1770 | [Maximum Score from Performing Multiplication Operations](https://leetcode.com/problems/maximum-score-from-performing-multiplication-operations/) | Hard | dp[i][j] pick from two ends |
| 1900 | [The Earliest and Latest Rounds Where Players Compete](https://leetcode.com/problems/the-earliest-and-latest-rounds-where-players-compete/) | Hard | memo over (n,first,second) tournament rounds |
| 2019 | [The Score of Students Solving Math Expression](https://leetcode.com/problems/the-score-of-students-solving-math-expression/) | Hard | dp[i][j] set of possible results, split k |
| 2312 | [Selling Pieces of Wood](https://leetcode.com/problems/selling-pieces-of-wood/) | Hard | dp[w][h] split rectangle horiz/vert cuts |
| 3277 | [Maximum XOR Score Subarray Queries](https://leetcode.com/problems/maximum-xor-score-subarray-queries/) | Hard | dp[i][j] max XOR score subarray range combine |
| 3441 | [Minimum Cost Good Caption](https://leetcode.com/problems/minimum-cost-good-caption/) | Hard | dp caption segments length>=3 min cost |
| 3500 | [Minimum Cost to Divide Array Into Subarrays](https://leetcode.com/problems/minimum-cost-to-divide-array-into-subarrays/) | Hard | dp[i] split array into subarrays cost |
| 3538 | [Merge Operations for Minimum Travel Time](https://leetcode.com/problems/merge-operations-for-minimum-travel-time/) | Hard | dp merge adjacent segments cost |
| 3563 | [Lexicographically Smallest String After Adjacent Removals](https://leetcode.com/problems/lexicographically-smallest-string-after-adjacent-removals/) | Hard | interval reducibility then greedy smallest |
| 3661 | [Maximum Walls Destroyed by Robots](https://leetcode.com/problems/maximum-walls-destroyed-by-robots/) | Hard | dp over sorted robots left/right wall coverage |
| 3743 | [Maximize Cyclic Partition Score](https://leetcode.com/problems/maximize-cyclic-partition-score/) | Hard | cyclic partition, range dp over cuts |
| 3801 | [Minimum Cost to Merge Sorted Lists](https://leetcode.com/problems/minimum-cost-to-merge-sorted-lists/) | Hard | dp[i][j] merge-cost over range |
| 3929 | [Minimum Partition Score II](https://leetcode.com/problems/minimum-partition-score-ii/) | Hard | dp partition minimize score over splits |

---

## Stock / State-Machine DP

**10 problems.** Model explicit states (hold / cash / cooldown) and transitions between them per day. Best-time-to-buy-sell family.

- **Recognize it when:** A small finite set of states with fixed legal transitions evolving over time.
- **Recurrence:** `hold[i]=max(hold[i-1], cash[i-1]-price)`, `cash[i]=max(cash[i-1], hold[i-1]+price-fee)`
- **Complexity:** Time `O(n·states·transactions)`, space `O(states)`.

| # | Problem | Difficulty | Core idea |
|---|---------|:----------:|-----------|
| 121 | [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | Easy | track min price, max profit |
| 122 | [Best Time to Buy and Sell Stock II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/) | Medium | greedy/state hold-vs-cash daily transition |
| 309 | [Best Time to Buy and Sell Stock with Cooldown](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/) | Medium | hold/sold/rest state transitions |
| 714 | [Best Time to Buy and Sell Stock with Transaction Fee](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/) | Medium | hold/cash states with fee |
| 1911 | [Maximum Alternating Subsequence Sum](https://leetcode.com/problems/maximum-alternating-subsequence-sum/) | Medium | even/odd pick state max sum |
| 3259 | [Maximum Energy Boost From Two Drinks](https://leetcode.com/problems/maximum-energy-boost-from-two-drinks/) | Medium | dp[i][drink] switch/stay states |
| 3573 | [Best Time to Buy and Sell Stock V](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-v/) | Medium | dp[i][k][state] buy/sell/short state machine |
| 123 | [Best Time to Buy and Sell Stock III](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/) | Hard | buy/sell states with at most 2 transactions |
| 188 | [Best Time to Buy and Sell Stock IV](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/) | Hard | dp[k][hold] buy/sell k transactions |
| 2361 | [Minimum Costs Using the Train Line](https://leetcode.com/problems/minimum-costs-using-the-train-line/) | Hard | dp regular/express hop states |

---

## Tree DP

**36 problems.** DP computed via post-order DFS; each node combines results from its children (often returns >1 value, e.g. rob/not-rob).

- **Recognize it when:** Input is a tree/BST; answer at a node needs children's answers first.
- **Recurrence:** `dfs(node) -> (take, skip)`; `take = node.val + sum(skip_child)`, `skip = sum(max(take,skip)_child)`.
- **Complexity:** Time `O(n)` one DFS pass, space `O(h)` recursion (rerooting adds a second pass).

| # | Problem | Difficulty | Core idea |
|---|---------|:----------:|-----------|
| 333 | [Largest BST Subtree](https://leetcode.com/problems/largest-bst-subtree/) | Medium | post-order return subtree BST info |
| 337 | [House Robber III](https://leetcode.com/problems/house-robber-iii/) | Medium | dp[node][rob/not] from children |
| 1372 | [Longest ZigZag Path in a Binary Tree](https://leetcode.com/problems/longest-zigzag-path-in-a-binary-tree/) | Medium | per-node zigzag left/right lengths |
| 2378 | [Choose Edges to Maximize Score in a Tree](https://leetcode.com/problems/choose-edges-to-maximize-score-in-a-tree/) | Medium | dp[node][taken] max score edges |
| 2673 | [Make Costs of Paths Equal in a Binary Tree](https://leetcode.com/problems/make-costs-of-paths-equal-in-a-binary-tree/) | Medium | post-order equalize child path costs |
| 2925 | [Maximum Score After Applying Operations on a Tree](https://leetcode.com/problems/maximum-score-after-applying-operations-on-a-tree/) | Medium | dfs keep-one-leaf per subtree |
| 3004 | [Maximum Subtree of the Same Color](https://leetcode.com/problems/maximum-subtree-of-the-same-color/) | Medium | postorder same-color subtree size |
| 3593 | [Minimum Increments to Equalize Leaf Paths](https://leetcode.com/problems/minimum-increments-to-equalize-leaf-paths/) | Medium | postorder equalize child path sums |
| 124 | [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | Hard | max down-path per node, update global |
| 834 | [Sum of Distances in Tree](https://leetcode.com/problems/sum-of-distances-in-tree/) | Hard | reroot subtree distance sums |
| 968 | [Binary Tree Cameras](https://leetcode.com/problems/binary-tree-cameras/) | Hard | post-order camera cover states |
| 1373 | [Maximum Sum BST in Binary Tree](https://leetcode.com/problems/maximum-sum-bst-in-binary-tree/) | Hard | postorder return BST range+sum |
| 1617 | [Count Subtrees With Max Distance Between Cities](https://leetcode.com/problems/count-subtrees-with-max-distance-between-cities/) | Hard | enumerate subtrees count max distance |
| 1896 | [Minimum Cost to Change the Final Value of Expression](https://leetcode.com/problems/minimum-cost-to-change-the-final-value-of-expression/) | Hard | dp expression tree value/flip cost |
| 1916 | [Count Ways to Build Rooms in an Ant Colony](https://leetcode.com/problems/count-ways-to-build-rooms-in-an-ant-colony/) | Hard | count topo orderings via subtree sizes |
| 2003 | [Smallest Missing Genetic Value in Each Subtree](https://leetcode.com/problems/smallest-missing-genetic-value-in-each-subtree/) | Hard | post-order gather missing genetic value per subtree |
| 2313 | [Minimum Flips in Binary Tree to Get Result](https://leetcode.com/problems/minimum-flips-in-binary-tree-to-get-result/) | Hard | dp[node][target] min flips postorder |
| 2538 | [Difference Between Maximum and Minimum Price Sum](https://leetcode.com/problems/difference-between-maximum-and-minimum-price-sum/) | Hard | reroot dp, max path sum dropping endpoint |
| 2581 | [Count Number of Possible Root Nodes](https://leetcode.com/problems/count-number-of-possible-root-nodes/) | Hard | rerooting to count valid roots |
| 2646 | [Minimize the Total Price of the Trips](https://leetcode.com/problems/minimize-the-total-price-of-the-trips/) | Hard | node frequencies via LCA + tree rob DP |
| 2846 | [Minimum Edge Weight Equilibrium Queries in a Tree](https://leetcode.com/problems/minimum-edge-weight-equilibrium-queries-in-a-tree/) | Hard | LCA plus edge-weight frequency counts |
| 2858 | [Minimum Edge Reversals So Every Node Is Reachable](https://leetcode.com/problems/minimum-edge-reversals-so-every-node-is-reachable/) | Hard | reroot count edge reversals |
| 2867 | [Count Valid Paths in a Tree](https://leetcode.com/problems/count-valid-paths-in-a-tree/) | Hard | dfs count prime-count paths in tree |
| 2920 | [Maximum Points After Collecting Coins From All Nodes](https://leetcode.com/problems/maximum-points-after-collecting-coins-from-all-nodes/) | Hard | tree dp with halving-coin state |
| 2973 | [Find Number of Coins to Place in Tree Nodes](https://leetcode.com/problems/find-number-of-coins-to-place-in-tree-nodes/) | Hard | post-order pick coin placement per subtree |
| 3068 | [Find the Maximum Sum of Node Values](https://leetcode.com/problems/find-the-maximum-sum-of-node-values/) | Hard | dp XOR parity max node sum |
| 3241 | [Time Taken to Mark All Nodes](https://leetcode.com/problems/time-taken-to-mark-all-nodes/) | Hard | reroot tree dp for max time |
| 3367 | [Maximize Sum of Weights after Edge Removals](https://leetcode.com/problems/maximize-sum-of-weights-after-edge-removals/) | Hard | tree dp keep/remove edges max weight |
| 3544 | [Subtree Inversion Sum](https://leetcode.com/problems/subtree-inversion-sum/) | Hard | subtree dp with inversion sign state |
| 3562 | [Maximum Profit from Trading Stocks with Discounts](https://leetcode.com/problems/maximum-profit-from-trading-stocks-with-discounts/) | Hard | tree knapsack with buy/sell budget |
| 3575 | [Maximum Good Subtree Score](https://leetcode.com/problems/maximum-good-subtree-score/) | Hard | per-subtree combine max score with pruning |
| 3585 | [Find Weighted Median Node in Tree](https://leetcode.com/problems/find-weighted-median-node-in-tree/) | Hard | weighted median via subtree/path distances |
| 3772 | [Maximum Subgraph Score in a Tree](https://leetcode.com/problems/maximum-subgraph-score-in-a-tree/) | Hard | post-order subtree score include/exclude |
| 3939 | [Count Non Adjacent Subsets in a Rooted Tree](https://leetcode.com/problems/count-non-adjacent-subsets-in-a-rooted-tree/) | Hard | non-adjacent subset counts include/exclude node |
| 3949 | [Subtree Inversion Sum II](https://leetcode.com/problems/subtree-inversion-sum-ii/) | Hard | subtree invert state dp max sum |
| 3973 | [Distinct Gate Paths to LCA](https://leetcode.com/problems/distinct-gate-paths-to-lca/) | Hard | count distinct root-to-LCA gate paths |

---

## Digit DP

**28 problems.** Count numbers `<= N` satisfying digit constraints. Recurse over digit positions carrying a `tight` (bounded) flag and problem state.

- **Recognize it when:** 'How many numbers up to N have property P on their digits'.
- **Recurrence:** `dp[pos][tight][state]` = sum over next digit `d in [0 .. (tight? N[pos]:9)]`.
- **Complexity:** Time `O(digits · states · 10)`, space `O(digits · states)`.

| # | Problem | Difficulty | Core idea |
|---|---------|:----------:|-----------|
| 3032 | [Count Numbers With Unique Digits II](https://leetcode.com/problems/count-numbers-with-unique-digits-ii/) | Easy | count unique-digit numbers in range via digit DP |
| 3954 | [Sum of Compatible Numbers in Range I](https://leetcode.com/problems/sum-of-compatible-numbers-in-range-i/) | Easy | count/sum numbers by digit compatibility |
| 788 | [Rotated Digits](https://leetcode.com/problems/rotated-digits/) | Medium | count rotated-good digits up to N |
| 3007 | [Maximum Number That Sum of the Prices Is Less Than or Equal to K](https://leetcode.com/problems/maximum-number-that-sum-of-the-prices-is-less-than-or-equal-to-k/) | Medium | bit dp count set-bit price sum |
| 3751 | [Total Waviness of Numbers in Range I](https://leetcode.com/problems/total-waviness-of-numbers-in-range-i/) | Medium | count waviness sum over digit numbers |
| 233 | [Number of Digit One](https://leetcode.com/problems/number-of-digit-one/) | Hard | count digit '1' occurrences up to N |
| 600 | [Non-negative Integers without Consecutive Ones](https://leetcode.com/problems/non-negative-integers-without-consecutive-ones/) | Hard | count no consecutive ones up to N bits |
| 902 | [Numbers At Most N Given Digit Set](https://leetcode.com/problems/numbers-at-most-n-given-digit-set/) | Hard | count numbers from digit set <= N |
| 1012 | [Numbers With Repeated Digits](https://leetcode.com/problems/numbers-with-repeated-digits/) | Hard | count numbers with repeated digits via mask |
| 1067 | [Digit Count in Range](https://leetcode.com/problems/digit-count-in-range/) | Hard | count digit occurrences in [low,high] via count(n) |
| 1397 | [Find All Good Strings](https://leetcode.com/problems/find-all-good-strings/) | Hard | digit dp with KMP evil-string state |
| 2376 | [Count Special Integers](https://leetcode.com/problems/count-special-integers/) | Hard | digit dp count distinct-digit numbers up to N |
| 2719 | [Count of Integers](https://leetcode.com/problems/count-of-integers/) | Hard | count integers with digit-sum bounds up to N |
| 2801 | [Count Stepping Numbers in Range](https://leetcode.com/problems/count-stepping-numbers-in-range/) | Hard | digit dp count stepping numbers in range |
| 2827 | [Number of Beautiful Integers in the Range](https://leetcode.com/problems/number-of-beautiful-integers-in-the-range/) | Hard | count integers with even/odd digit balance divisible |
| 2999 | [Count the Number of Powerful Integers](https://leetcode.com/problems/count-the-number-of-powerful-integers/) | Hard | count numbers with suffix, digit limit |
| 3260 | [Find the Largest Palindrome Divisible by K](https://leetcode.com/problems/find-the-largest-palindrome-divisible-by-k/) | Hard | build palindrome digits divisible by K |
| 3352 | [Count K-Reducible Numbers Less Than N](https://leetcode.com/problems/count-k-reducible-numbers-less-than-n/) | Hard | digit dp count popcount-reducible < N |
| 3448 | [Count Substrings Divisible By Last Digit](https://leetcode.com/problems/count-substrings-divisible-by-last-digit/) | Hard | digit dp count substrings divisible by last digit |
| 3490 | [Count Beautiful Numbers](https://leetcode.com/problems/count-beautiful-numbers/) | Hard | count numbers by digit-sum divides product |
| 3519 | [Count Numbers with Non-Decreasing Digits](https://leetcode.com/problems/count-numbers-with-non-decreasing-digits/) | Hard | digit dp non-decreasing digits in base |
| 3533 | [Concatenated Divisibility](https://leetcode.com/problems/concatenated-divisibility/) | Hard | dp over positions tracking remainder mod k |
| 3621 | [Number of Integers With Popcount-Depth Equal to K I](https://leetcode.com/problems/number-of-integers-with-popcount-depth-equal-to-k-i/) | Hard | count numbers by popcount-depth via digit DP |
| 3704 | [Count No-Zero Pairs That Sum to N](https://leetcode.com/problems/count-no-zero-pairs-that-sum-to-n/) | Hard | count no-zero digit pairs summing to N |
| 3753 | [Total Waviness of Numbers in Range II](https://leetcode.com/problems/total-waviness-of-numbers-in-range-ii/) | Hard | sum waviness of numbers in range via digit DP |
| 3791 | [Number of Balanced Integers in a Range](https://leetcode.com/problems/number-of-balanced-integers-in-a-range/) | Hard | digit dp balanced digit-sum in range |
| 3869 | [Count Fancy Numbers in a Range](https://leetcode.com/problems/count-fancy-numbers-in-a-range/) | Hard | count numbers with digit constraints in range |
| 3966 | [Count Good Integers in a Range](https://leetcode.com/problems/count-good-integers-in-a-range/) | Hard | count good integers in range digit dp |

---

## Bitmask DP

**44 problems.** State encodes a SUBSET as an integer bitmask. Assignment / TSP / cover problems where `n <= ~20`.

- **Recognize it when:** You must track exactly which elements are used; order or pairing matters.
- **Recurrence:** `dp[mask] = best over i in mask of dp[mask ^ (1<<i)] + cost(...)`
- **Complexity:** Time `O(2^n · n)` (or `·n^2`), space `O(2^n)`. Only feasible for small `n`.

| # | Problem | Difficulty | Core idea |
|---|---------|:----------:|-----------|
| 351 | [Android Unlock Patterns](https://leetcode.com/problems/android-unlock-patterns/) | Medium | visited-cell bitmask DFS paths |
| 473 | [Matchsticks to Square](https://leetcode.com/problems/matchsticks-to-square/) | Medium | subset-sum into 4 equal sides |
| 526 | [Beautiful Arrangement](https://leetcode.com/problems/beautiful-arrangement/) | Medium | mask of used numbers at position |
| 698 | [Partition to K Equal Sum Subsets](https://leetcode.com/problems/partition-to-k-equal-sum-subsets/) | Medium | subset bitmask fill k buckets |
| 1066 | [Campus Bikes II](https://leetcode.com/problems/campus-bikes-ii/) | Medium | assign bikes to workers subset mask |
| 1947 | [Maximum Compatibility Score Sum](https://leetcode.com/problems/maximum-compatibility-score-sum/) | Medium | assignment bitmask compatibility |
| 1986 | [Minimum Number of Work Sessions to Finish the Tasks](https://leetcode.com/problems/minimum-number-of-work-sessions-to-finish-the-tasks/) | Medium | dp[mask]=(sessions,time) subset assignment |
| 2152 | [Minimum Number of Lines to Cover Points](https://leetcode.com/problems/minimum-number-of-lines-to-cover-points/) | Medium | cover points by lines over mask |
| 2305 | [Fair Distribution of Cookies](https://leetcode.com/problems/fair-distribution-of-cookies/) | Medium | distribute cookie-subsets over children |
| 2572 | [Count the Number of Square-Free Subsets](https://leetcode.com/problems/count-the-number-of-square-free-subsets/) | Medium | prime-factor mask subset product |
| 2741 | [Special Permutations](https://leetcode.com/problems/special-permutations/) | Medium | bitmask permutation with adjacency divisibility |
| 2850 | [Minimum Moves to Spread Stones Over Grid](https://leetcode.com/problems/minimum-moves-to-spread-stones-over-grid/) | Medium | min-cost assignment of extra stones to holes |
| 2992 | [Number of Self-Divisible Permutations](https://leetcode.com/problems/number-of-self-divisible-permutations/) | Medium | permutation count over used-mask |
| 3376 | [Minimum Time to Break Locks I](https://leetcode.com/problems/minimum-time-to-break-locks-i/) | Medium | dp over broken-lock subset, order |
| 3670 | [Maximum Product of Two Integers With No Common Bits](https://leetcode.com/problems/maximum-product-of-two-integers-with-no-common-bits/) | Medium | submask dp disjoint-bit max product |
| 465 | [Optimal Account Balancing](https://leetcode.com/problems/optimal-account-balancing/) | Hard | dp over debt subset settlements |
| 691 | [Stickers to Spell Word](https://leetcode.com/problems/stickers-to-spell-word/) | Hard | dp[mask] over covered target letters |
| 847 | [Shortest Path Visiting All Nodes](https://leetcode.com/problems/shortest-path-visiting-all-nodes/) | Hard | BFS state (node,visited bitmask) |
| 943 | [Find the Shortest Superstring](https://leetcode.com/problems/find-the-shortest-superstring/) | Hard | TSP over word overlaps, subset+last |
| 996 | [Number of Squareful Arrays](https://leetcode.com/problems/number-of-squareful-arrays/) | Hard | permutation dp over used mask, squareful edges |
| 1125 | [Smallest Sufficient Team](https://leetcode.com/problems/smallest-sufficient-team/) | Hard | skill-set bitmask min team |
| 1255 | [Maximum Score Words Formed by Letters](https://leetcode.com/problems/maximum-score-words-formed-by-letters/) | Hard | subset enumeration of words respecting letter counts |
| 1349 | [Maximum Students Taking Exam](https://leetcode.com/problems/maximum-students-taking-exam/) | Hard | dp[row][mask] valid seatings vs prev row |
| 1434 | [Number of Ways to Wear Different Hats to Each Other](https://leetcode.com/problems/number-of-ways-to-wear-different-hats-to-each-other/) | Hard | assign hats over people-subset mask |
| 1494 | [Parallel Courses II](https://leetcode.com/problems/parallel-courses-ii/) | Hard | dp over course subset masks per semester |
| 1595 | [Minimum Cost to Connect Two Groups of Points](https://leetcode.com/problems/minimum-cost-to-connect-two-groups-of-points/) | Hard | dp over group1 index, mask of group2 |
| 1655 | [Distribute Repeating Integers](https://leetcode.com/problems/distribute-repeating-integers/) | Hard | dp over customer subset assignments |
| 1659 | [Maximize Grid Happiness](https://leetcode.com/problems/maximize-grid-happiness/) | Hard | profile/broken-profile bitmask over rows |
| 1681 | [Minimum Incompatibility](https://leetcode.com/problems/minimum-incompatibility/) | Hard | dp over subsets forming k groups |
| 1723 | [Find Minimum Time to Finish All Jobs](https://leetcode.com/problems/find-minimum-time-to-finish-all-jobs/) | Hard | dp assign jobs subset to workers |
| 1799 | [Maximize Score After N Operations](https://leetcode.com/problems/maximize-score-after-n-operations/) | Hard | dp[mask] pair up with gcd*operation index |
| 1815 | [Maximum Number of Groups Getting Fresh Donuts](https://leetcode.com/problems/maximum-number-of-groups-getting-fresh-donuts/) | Hard | dp over remainder-count state, memoize |
| 1879 | [Minimum XOR Sum of Two Arrays](https://leetcode.com/problems/minimum-xor-sum-of-two-arrays/) | Hard | assignment bitmask min XOR sum |
| 1931 | [Painting a Grid With Three Different Colors](https://leetcode.com/problems/painting-a-grid-with-three-different-colors/) | Hard | column color-pattern states transitions |
| 1994 | [The Number of Good Subsets](https://leetcode.com/problems/the-number-of-good-subsets/) | Hard | subset product of primes bitmask |
| 2172 | [Maximum AND Sum of Array](https://leetcode.com/problems/maximum-and-sum-of-array/) | Hard | dp over slot bitmask assigning numbers to k slots |
| 2247 | [Maximum Cost of Trip With K Highways](https://leetcode.com/problems/maximum-cost-of-trip-with-k-highways/) | Hard | dp[city][visited mask] K edges |
| 2403 | [Minimum Time to Kill All Monsters](https://leetcode.com/problems/minimum-time-to-kill-all-monsters/) | Hard | subset of killed monsters, min time |
| 3149 | [Find the Minimum Cost Array Permutation](https://leetcode.com/problems/find-the-minimum-cost-array-permutation/) | Hard | permutation bitmask min cost |
| 3276 | [Select Cells in Grid With Maximum Score](https://leetcode.com/problems/select-cells-in-grid-with-maximum-score/) | Hard | dp assign rows to value bitmask |
| 3287 | [Find the Maximum Sequence Value of Array](https://leetcode.com/problems/find-the-maximum-sequence-value-of-array/) | Hard | prefix/suffix OR-value dp over subsequences |
| 3539 | [Find Sum of Array Product of Magical Sequences](https://leetcode.com/problems/find-sum-of-array-product-of-magical-sequences/) | Hard | dp over chosen index mask with carry/count |
| 3615 | [Longest Palindromic Path in Graph](https://leetcode.com/problems/longest-palindromic-path-in-graph/) | Hard | bitmask visited-nodes palindromic path |
| 3989 | [Maximum Consistent Columns in a Grid](https://leetcode.com/problems/maximum-consistent-columns-in-a-grid/) | Hard | column patterns via row masks |

---

## Counting / Combinatorial DP

**85 problems.** Count the number of ways rather than optimize a value. Catalan numbers, tilings, arrangements, sequence counts (often mod 1e9+7).

- **Recognize it when:** Question asks 'how many ways / arrangements / distinct results'.
- **Recurrence:** `dp[i] = sum of dp[j]` over valid predecessors; combine with multiplication for independent choices.
- **Complexity:** Time depends on structure; watch for modular arithmetic on every add/multiply.

| # | Problem | Difficulty | Core idea |
|---|---------|:----------:|-----------|
| 118 | [Pascal's Triangle](https://leetcode.com/problems/pascals-triangle/) | Easy | row[j]=prev[j-1]+prev[j] |
| 119 | [Pascal's Triangle II](https://leetcode.com/problems/pascals-triangle-ii/) | Easy | row from previous row sums |
| 22 | [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) | Medium | backtracking build valid paren strings |
| 95 | [Unique Binary Search Trees II](https://leetcode.com/problems/unique-binary-search-trees-ii/) | Medium | build BSTs by choosing each root, combine left/right subtrees |
| 96 | [Unique Binary Search Trees](https://leetcode.com/problems/unique-binary-search-trees/) | Medium | Catalan: sum over root splits left*right |
| 357 | [Count Numbers with Unique Digits](https://leetcode.com/problems/count-numbers-with-unique-digits/) | Medium | count distinct-digit numbers by length |
| 634 | [Find the Derangement of An Array](https://leetcode.com/problems/find-the-derangement-of-an-array/) | Medium | D(n)=(n-1)(D(n-1)+D(n-2)) |
| 750 | [Number Of Corner Rectangles](https://leetcode.com/problems/number-of-corner-rectangles/) | Medium | count row pairs sharing columns, choose 2 |
| 823 | [Binary Trees With Factors](https://leetcode.com/problems/binary-trees-with-factors/) | Medium | dp[v]=sum dp[a]*dp[b] for factor pairs |
| 894 | [All Possible Full Binary Trees](https://leetcode.com/problems/all-possible-full-binary-trees/) | Medium | combine left/right subtree counts by odd split |
| 935 | [Knight Dialer](https://leetcode.com/problems/knight-dialer/) | Medium | count knight-move digit sequences |
| 1524 | [Number of Sub-arrays With Odd Sum](https://leetcode.com/problems/number-of-sub-arrays-with-odd-sum/) | Medium | prefix parity counts of subarrays |
| 1525 | [Number of Good Ways to Split a String](https://leetcode.com/problems/number-of-good-ways-to-split-a-string/) | Medium | prefix/suffix distinct-char counts split |
| 1621 | [Number of Sets of K Non-Overlapping Line Segments](https://leetcode.com/problems/number-of-sets-of-k-non-overlapping-line-segments/) | Medium | dp[i][k] count segments ending at i |
| 1641 | [Count Sorted Vowel Strings](https://leetcode.com/problems/count-sorted-vowel-strings/) | Medium | dp[len][last-vowel] nondecreasing count |
| 2063 | [Vowels of All Substrings](https://leetcode.com/problems/vowels-of-all-substrings/) | Medium | contribution of each vowel by position i*(n-i) |
| 2189 | [Number of Ways to Build House of Cards](https://leetcode.com/problems/number-of-ways-to-build-house-of-cards/) | Medium | dp[cards][rows] ways build houses |
| 2222 | [Number of Ways to Select Buildings](https://leetcode.com/problems/number-of-ways-to-select-buildings/) | Medium | count 010/101 via prefix char counts |
| 2393 | [Count Strictly Increasing Subarrays](https://leetcode.com/problems/count-strictly-increasing-subarrays/) | Medium | count increasing runs sum lengths |
| 2400 | [Number of Ways to Reach a Position After Exactly k Steps](https://leetcode.com/problems/number-of-ways-to-reach-a-position-after-exactly-k-steps/) | Medium | combinatorics C(k,(k+d)/2) reachable paths |
| 2466 | [Count Ways To Build Good Strings](https://leetcode.com/problems/count-ways-to-build-good-strings/) | Medium | dp[len]=dp[len-zero]+dp[len-one] |
| 2495 | [Number of Subarrays Having Even Product](https://leetcode.com/problems/number-of-subarrays-having-even-product/) | Medium | count subarrays via parity prefixes |
| 2533 | [Number of Good Binary Strings](https://leetcode.com/problems/number-of-good-binary-strings/) | Medium | dp[len] count binary strings with run constraints |
| 2597 | [The Number of Beautiful Subsets](https://leetcode.com/problems/the-number-of-beautiful-subsets/) | Medium | group by mod, house-robber count |
| 2638 | [Count the Number of K-Free Subsets](https://leetcode.com/problems/count-the-number-of-k-free-subsets/) | Medium | house-robber per residue chain product |
| 2750 | [Ways to Split Array Into Good Subarrays](https://leetcode.com/problems/ways-to-split-array-into-good-subarrays/) | Medium | dp multiply gaps between consecutive ones |
| 2930 | [Number of Strings Which Can Be Rearranged to Contain Substring](https://leetcode.com/problems/number-of-strings-which-can-be-rearranged-to-contain-substring/) | Medium | dp over positions tracking l,e,t state |
| 3129 | [Find All Possible Stable Binary Arrays I](https://leetcode.com/problems/find-all-possible-stable-binary-arrays-i/) | Medium | dp[i][j][last] count arrays run-limit |
| 3247 | [Number of Subsequences with Odd Sum](https://leetcode.com/problems/number-of-subsequences-with-odd-sum/) | Medium | count odd/even sum subsequences |
| 3335 | [Total Characters in String After Transformations I](https://leetcode.com/problems/total-characters-in-string-after-transformations-i/) | Medium | dp over char counts after t transforms |
| 3339 | [Find the Number of K-Even Arrays](https://leetcode.com/problems/find-the-number-of-k-even-arrays/) | Medium | dp[i][evenCount][parity] count k-even arrays |
| 3388 | [Count Beautiful Splits in an Array](https://leetcode.com/problems/count-beautiful-splits-in-an-array/) | Medium | prefix-match Z-array count valid three-way splits |
| 3428 | [Maximum and Minimum Sums of at Most Size K Subsequences](https://leetcode.com/problems/maximum-and-minimum-sums-of-at-most-size-k-subsequences/) | Medium | sorted subsequence min/max contributions |
| 3524 | [Find X Value of Array I](https://leetcode.com/problems/find-x-value-of-array-i/) | Medium | dp over remove suffix product mod values |
| 3578 | [Count Partitions With Max-Min Difference at Most K](https://leetcode.com/problems/count-partitions-with-max-min-difference-at-most-k/) | Medium | dp partitions with sliding-window sorted values |
| 3811 | [Number of Alternating XOR Partitions](https://leetcode.com/problems/number-of-alternating-xor-partitions/) | Medium | dp count partitions by XOR prefix state |
| 446 | [Arithmetic Slices II - Subsequence](https://leetcode.com/problems/arithmetic-slices-ii-subsequence/) | Hard | dp[i][diff] count arithmetic subseq by common diff |
| 629 | [K Inverse Pairs Array](https://leetcode.com/problems/k-inverse-pairs-array/) | Hard | dp[n][k] inverse pairs with sliding window sum |
| 903 | [Valid Permutations for DI Sequence](https://leetcode.com/problems/valid-permutations-for-di-sequence/) | Hard | dp[i][j] permutations by rank, prefix sums |
| 920 | [Number of Music Playlists](https://leetcode.com/problems/number-of-music-playlists/) | Hard | dp[i][j] songs placed with j distinct |
| 940 | [Distinct Subsequences II](https://leetcode.com/problems/distinct-subsequences-ii/) | Hard | dp counting distinct subsequences by last char |
| 1223 | [Dice Roll Simulation](https://leetcode.com/problems/dice-roll-simulation/) | Hard | dp[roll][face][consec] count sequences |
| 1269 | [Number of Ways to Stay in the Same Place After Some Steps](https://leetcode.com/problems/number-of-ways-to-stay-in-the-same-place-after-some-steps/) | Hard | dp[steps][pos] ways to return |
| 1359 | [Count All Valid Pickup and Delivery Options](https://leetcode.com/problems/count-all-valid-pickup-and-delivery-options/) | Hard | combinatorial recurrence over n pairs |
| 1411 | [Number of Ways to Paint N × 3 Grid](https://leetcode.com/problems/number-of-ways-to-paint-n-3-grid/) | Hard | row color-pattern transitions count |
| 1420 | [Build Array Where You Can Find The Maximum Exactly K Comparisons](https://leetcode.com/problems/build-array-where-you-can-find-the-maximum-exactly-k-comparisons/) | Hard | dp[i][max][cost] build array count |
| 1569 | [Number of Ways to Reorder Array to Get Same BST](https://leetcode.com/problems/number-of-ways-to-reorder-array-to-get-same-bst/) | Hard | combinatorics over BST subtrees |
| 1643 | [Kth Smallest Instructions](https://leetcode.com/problems/kth-smallest-instructions/) | Hard | kth lexicographic path via binomial counts |
| 1692 | [Count Ways to Distribute Candies](https://leetcode.com/problems/count-ways-to-distribute-candies/) | Hard | Stirling-like dp[i][k] bags recurrence |
| 1735 | [Count Ways to Make Array With Product](https://leetcode.com/problems/count-ways-to-make-array-with-product/) | Hard | factorization stars-and-bars counting |
| 1866 | [Number of Ways to Rearrange Sticks With K Sticks Visible](https://leetcode.com/problems/number-of-ways-to-rearrange-sticks-with-k-sticks-visible/) | Hard | dp[n][k] Stirling-like place tallest stick |
| 1955 | [Count Number of Special Subsequences](https://leetcode.com/problems/count-number-of-special-subsequences/) | Hard | dp[state] counting subsequences 0<1<2 |
| 1977 | [Number of Ways to Separate Numbers](https://leetcode.com/problems/number-of-ways-to-separate-numbers/) | Hard | dp[i][len] partition digits, LCP compare |
| 1987 | [Number of Unique Good Subsequences](https://leetcode.com/problems/number-of-unique-good-subsequences/) | Hard | count distinct subsequences by last char |
| 2143 | [Choose Numbers From Two Arrays in Range](https://leetcode.com/problems/choose-numbers-from-two-arrays-in-range/) | Hard | dp[i][diff] count picks two arrays |
| 2147 | [Number of Ways to Divide a Long Corridor](https://leetcode.com/problems/number-of-ways-to-divide-a-long-corridor/) | Hard | count seat divisions between pairs of seats |
| 2262 | [Total Appeal of A String](https://leetcode.com/problems/total-appeal-of-a-string/) | Hard | dp[i] appeal contribution by last occurrence |
| 2318 | [Number of Distinct Roll Sequences](https://leetcode.com/problems/number-of-distinct-roll-sequences/) | Hard | dp[len][prev][prevprev] valid roll sequences |
| 2338 | [Count the Number of Ideal Arrays](https://leetcode.com/problems/count-the-number-of-ideal-arrays/) | Hard | multiplicative chains times combinations |
| 2552 | [Count Increasing Quadruplets](https://leetcode.com/problems/count-increasing-quadruplets/) | Hard | prefix counts over index pairs |
| 2681 | [Power of Heroes](https://leetcode.com/problems/power-of-heroes/) | Hard | sorted contribution dp accumulation |
| 2912 | [Number of Ways to Reach Destination in the Grid](https://leetcode.com/problems/number-of-ways-to-reach-destination-in-the-grid/) | Hard | combinatorial lattice paths with moves |
| 3082 | [Find the Sum of the Power of All Subsequences](https://leetcode.com/problems/find-the-sum-of-the-power-of-all-subsequences/) | Hard | knapsack counting with power-of-two weights |
| 3130 | [Find All Possible Stable Binary Arrays II](https://leetcode.com/problems/find-all-possible-stable-binary-arrays-ii/) | Hard | dp counts of stable binary arrays |
| 3154 | [Find Number of Ways to Reach the K-th Stair](https://leetcode.com/problems/find-number-of-ways-to-reach-the-k-th-stair/) | Hard | count ways with up/down jump states, memo |
| 3193 | [Count the Number of Inversions](https://leetcode.com/problems/count-the-number-of-inversions/) | Hard | insertion DP counting inversions dp[i][j] |
| 3250 | [Find the Count of Monotonic Pairs I](https://leetcode.com/problems/find-the-count-of-monotonic-pairs-i/) | Hard | dp[i][val] monotonic non-dec/non-inc pair counts |
| 3251 | [Find the Count of Monotonic Pairs II](https://leetcode.com/problems/find-the-count-of-monotonic-pairs-ii/) | Hard | dp over pairs with prefix-sum monotonic constraints |
| 3299 | [Sum of Consecutive Subsequences](https://leetcode.com/problems/sum-of-consecutive-subsequences/) | Hard | dp sum over consecutive value chains |
| 3317 | [Find the Number of Possible Ways for an Event](https://leetcode.com/problems/find-the-number-of-possible-ways-for-an-event/) | Hard | Stirling-like counting of assignments |
| 3320 | [Count The Number of Winning Sequences](https://leetcode.com/problems/count-the-number-of-winning-sequences/) | Hard | dp count sequences by last move+score |
| 3333 | [Find the Original Typed String II](https://leetcode.com/problems/find-the-original-typed-string-ii/) | Hard | dp count original strings, group run lengths |
| 3336 | [Find the Number of Subsequences With Equal GCD](https://leetcode.com/problems/find-the-number-of-subsequences-with-equal-gcd/) | Hard | dp count subsequences by gcd pairs |
| 3337 | [Total Characters in String After Transformations II](https://leetcode.com/problems/total-characters-in-string-after-transformations-ii/) | Hard | matrix-exponent letter count transitions |
| 3343 | [Count Number of Balanced Permutations](https://leetcode.com/problems/count-number-of-balanced-permutations/) | Hard | count perms by digit sum split, multinomial dp |
| 3389 | [Minimum Operations to Make Character Frequencies Equal](https://leetcode.com/problems/minimum-operations-to-make-character-frequencies-equal/) | Hard | dp over target frequency, min char ops |
| 3559 | [Number of Ways to Assign Edge Weights II](https://leetcode.com/problems/number-of-ways-to-assign-edge-weights-ii/) | Hard | count parity-weight assignments via combinatorics dp |
| 3686 | [Number of Stable Subsequences](https://leetcode.com/problems/number-of-stable-subsequences/) | Hard | dp counting stable subsequences by parity run |
| 3699 | [Number of ZigZag Arrays I](https://leetcode.com/problems/number-of-zigzag-arrays-i/) | Hard | dp[i][v] zigzag arrays by direction |
| 3700 | [Number of ZigZag Arrays II](https://leetcode.com/problems/number-of-zigzag-arrays-ii/) | Hard | zigzag arrays dp with matrix power |
| 3725 | [Count Ways to Choose Coprime Integers from Rows](https://leetcode.com/problems/count-ways-to-choose-coprime-integers-from-rows/) | Hard | count coprime pairs via mobius/gcd counts |
| 3757 | [Number of Effective Subsequences](https://leetcode.com/problems/number-of-effective-subsequences/) | Hard | count subsequences with effective condition dp |
| 3850 | [Count Sequences to K](https://leetcode.com/problems/count-sequences-to-k/) | Hard | dp counting sequences reaching sum K |
| 3883 | [Count Non Decreasing Arrays With Given Digit Sums](https://leetcode.com/problems/count-non-decreasing-arrays-with-given-digit-sums/) | Hard | count nondecreasing arrays by digit sum |
| 3916 | [Number of ZigZag Arrays III](https://leetcode.com/problems/number-of-zigzag-arrays-iii/) | Hard | dp count zigzag arrays by direction |

---

## Kadane / Max-Subarray DP

**15 problems.** The 1-variable running-optimum trick: best subarray ending here. Extends to products, circular arrays, alternating signs.

- **Recognize it when:** Contiguous subarray max/min sum or product; single left-to-right sweep.
- **Recurrence:** `cur = max(a[i], cur + a[i]); best = max(best, cur)` (track min too for products).
- **Complexity:** Time `O(n)`, space `O(1)`.

| # | Problem | Difficulty | Core idea |
|---|---------|:----------:|-----------|
| 53 | [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | Medium | dp[i]=max(a[i],dp[i-1]+a[i]) |
| 152 | [Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) | Medium | track max/min product ending at i |
| 918 | [Maximum Sum Circular Subarray](https://leetcode.com/problems/maximum-sum-circular-subarray/) | Medium | Kadane max + circular via total-min |
| 1014 | [Best Sightseeing Pair](https://leetcode.com/problems/best-sightseeing-pair/) | Medium | track best A[i]+i as scan, add A[j]-j |
| 1031 | [Maximum Sum of Two Non-Overlapping Subarrays](https://leetcode.com/problems/maximum-sum-of-two-non-overlapping-subarrays/) | Medium | prefix sums, best fixed-len window pair |
| 1186 | [Maximum Subarray Sum with One Deletion](https://leetcode.com/problems/maximum-subarray-sum-with-one-deletion/) | Medium | Kadane with 0/1 deletion states |
| 1191 | [K-Concatenation Maximum Sum](https://leetcode.com/problems/k-concatenation-maximum-sum/) | Medium | kadane on concatenated array |
| 1746 | [Maximum Subarray Sum After One Operation](https://leetcode.com/problems/maximum-subarray-sum-after-one-operation/) | Medium | Kadane with one squaring operation |
| 1749 | [Maximum Absolute Sum of Any Subarray](https://leetcode.com/problems/maximum-absolute-sum-of-any-subarray/) | Medium | track max and min subarray sums simultaneously |
| 2036 | [Maximum Alternating Subarray Sum](https://leetcode.com/problems/maximum-alternating-subarray-sum/) | Medium | Kadane alternating sign state |
| 2606 | [Find the Substring With Maximum Cost](https://leetcode.com/problems/find-the-substring-with-maximum-cost/) | Medium | Kadane on weighted char values max subarray |
| 3976 | [Maximum Subarray Sum After Multiplier](https://leetcode.com/problems/maximum-subarray-sum-after-multiplier/) | Medium | Kadane variant with multiplier on subarray sum |
| 2272 | [Substring With Largest Variance](https://leetcode.com/problems/substring-with-largest-variance/) | Hard | Kadane variance per char pair, force one negative |
| 2321 | [Maximum Score Of Spliced Array](https://leetcode.com/problems/maximum-score-of-spliced-array/) | Hard | max subarray of difference nums2-nums1 both ways |
| 3410 | [Maximize Subarray Sum After Removing All Occurrences of One Element](https://leetcode.com/problems/maximize-subarray-sum-after-removing-all-occurrences-of-one-element/) | Hard | Kadane with option to remove one repeated element |

---

## Game Theory (Minimax) DP

**15 problems.** Two players play optimally; you compute the outcome via minimax. Score-difference framing turns it into a clean max.

- **Recognize it when:** Adversarial turn-based game: stone game, predict-the-winner, Nim-like, can-I-win.
- **Recurrence:** `dp[i][j] = max(a[i]-dp[i+1][j], a[j]-dp[i][j-1])` (current player maximizes own margin).
- **Complexity:** Time `O(n^2)` interval-style, space `O(n^2)`; bitmask states for set-based games.

| # | Problem | Difficulty | Core idea |
|---|---------|:----------:|-----------|
| 1025 | [Divisor Game](https://leetcode.com/problems/divisor-game/) | Easy | two-player optimal parity/divisor play |
| 294 | [Flip Game II](https://leetcode.com/problems/flip-game-ii/) | Medium | win if any move leaves losing state |
| 464 | [Can I Win](https://leetcode.com/problems/can-i-win/) | Medium | bitmask state, minimax win check |
| 486 | [Predict the Winner](https://leetcode.com/problems/predict-the-winner/) | Medium | dp[i][j] max score diff, two players |
| 877 | [Stone Game](https://leetcode.com/problems/stone-game/) | Medium | interval minimax score difference |
| 1140 | [Stone Game II](https://leetcode.com/problems/stone-game-ii/) | Medium | minimax dp[i][M] suffix take |
| 1690 | [Stone Game VII](https://leetcode.com/problems/stone-game-vii/) | Medium | interval dp score-diff two players |
| 1908 | [Game of Nim](https://leetcode.com/problems/game-of-nim/) | Medium | nim/grundy two-player optimal |
| 3984 | [Divisible Game](https://leetcode.com/problems/divisible-game/) | Medium | win if divisor move leaves losing state |
| 913 | [Cat and Mouse](https://leetcode.com/problems/cat-and-mouse/) | Hard | minimax over positions+turn, BFS states |
| 1406 | [Stone Game III](https://leetcode.com/problems/stone-game-iii/) | Hard | dp[i] suffix score two-player optimal take 1-3 |
| 1510 | [Stone Game IV](https://leetcode.com/problems/stone-game-iv/) | Hard | dp[n] win if any move to loss |
| 1728 | [Cat and Mouse II](https://leetcode.com/problems/cat-and-mouse-ii/) | Hard | cat-mouse minimax memo over positions+turn |
| 1872 | [Stone Game VIII](https://leetcode.com/problems/stone-game-viii/) | Hard | prefix-sum suffix dp optimal score diff |
| 2005 | [Subtree Removal Game with Fibonacci Tree](https://leetcode.com/problems/subtree-removal-game-with-fibonacci-tree/) | Hard | Fibonacci tree Grundy/parity game |

---

## DP on Graphs (shortest-path / DAG)

**22 problems.** DP over graph nodes: longest path on a DAG, layered Bellman-Ford, or Dijkstra combined with path counting.

- **Recognize it when:** Transitions follow graph edges; either the graph is a DAG (topo order) or you need shortest-path relaxation.
- **Recurrence:** `dp[v] = combine over edges (u->v) of dp[u] + w(u,v)`; process in topo order for DAGs.
- **Complexity:** Time `O(V+E)` on a DAG; `O(E log V)` when layered on Dijkstra.

| # | Problem | Difficulty | Core idea |
|---|---------|:----------:|-----------|
| 787 | [Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/) | Medium | Bellman-Ford k stops dp |
| 1334 | [Find the City With the Smallest Number of Neighbors at a Threshold Distance](https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/) | Medium | Floyd-Warshall all-pairs shortest paths |
| 1786 | [Number of Restricted Paths From First to Last Node](https://leetcode.com/problems/number-of-restricted-paths-from-first-to-last-node/) | Medium | Dijkstra distances + DAG path count |
| 1976 | [Number of Ways to Arrive at Destination](https://leetcode.com/problems/number-of-ways-to-arrive-at-destination/) | Medium | Dijkstra + count shortest paths |
| 3543 | [Maximum Weighted K-Edge Path](https://leetcode.com/problems/maximum-weighted-k-edge-path/) | Medium | max-weight path with k edges |
| 329 | [Longest Increasing Path in a Matrix](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/) | Hard | memo DFS longest path on DAG |
| 568 | [Maximum Vacation Days](https://leetcode.com/problems/maximum-vacation-days/) | Hard | dp[week][city] max vacation over flight graph |
| 773 | [Sliding Puzzle](https://leetcode.com/problems/sliding-puzzle/) | Hard | BFS shortest path over board states |
| 1548 | [The Most Similar Path in a Graph](https://leetcode.com/problems/the-most-similar-path-in-a-graph/) | Hard | dp[step][node] min edit dist path |
| 1857 | [Largest Color Value in a Directed Graph](https://leetcode.com/problems/largest-color-value-in-a-directed-graph/) | Hard | topo-order color-count longest path |
| 1928 | [Minimum Cost to Reach Destination in Time](https://leetcode.com/problems/minimum-cost-to-reach-destination-in-time/) | Hard | dp[node][time] min cost with time budget |
| 2050 | [Parallel Courses III](https://leetcode.com/problems/parallel-courses-iii/) | Hard | longest path DAG topological order |
| 2127 | [Maximum Employees to Be Invited to a Meeting](https://leetcode.com/problems/maximum-employees-to-be-invited-to-a-meeting/) | Hard | functional graph cycles + chains |
| 2328 | [Number of Increasing Paths in a Grid](https://leetcode.com/problems/number-of-increasing-paths-in-a-grid/) | Hard | memo increasing paths over grid DAG |
| 2617 | [Minimum Number of Visited Cells in a Grid](https://leetcode.com/problems/minimum-number-of-visited-cells-in-a-grid/) | Hard | BFS/dp min visited cells reachable |
| 2876 | [Count Visited Nodes in a Directed Graph](https://leetcode.com/problems/count-visited-nodes-in-a-directed-graph/) | Hard | functional graph count reachable via cycle detection |
| 3530 | [Maximum Profit from Valid Topological Order in DAG](https://leetcode.com/problems/maximum-profit-from-valid-topological-order-in-dag/) | Hard | DP over topological orders maximizing profit |
| 3534 | [Path Existence Queries in a Graph II](https://leetcode.com/problems/path-existence-queries-in-a-graph-ii/) | Hard | binary lifting shortest reachable path queries |
| 3553 | [Minimum Weighted Subgraph With the Required Paths II](https://leetcode.com/problems/minimum-weighted-subgraph-with-the-required-paths-ii/) | Hard | multi-source dijkstra combine paths |
| 3620 | [Network Recovery Pathways](https://leetcode.com/problems/network-recovery-pathways/) | Hard | binary-search + DAG longest path feasibility |
| 3977 | [Minimum Time to Reach Target With Limited Power](https://leetcode.com/problems/minimum-time-to-reach-target-with-limited-power/) | Hard | Dijkstra/DP over node+power states |
| 3995 | [Minimum Cost to Convert String III](https://leetcode.com/problems/minimum-cost-to-convert-string-iii/) | Hard | Floyd-Warshall costs + dp[i] substring convert |

---

## Probability / Expectation DP

**8 problems.** States hold probabilities or expected values; transitions weight successors by their probability.

- **Recognize it when:** 'Probability of ...' or 'expected value of ...' with random transitions.
- **Recurrence:** `E[state] = sum over outcomes p(outcome) · (reward + E[next])`
- **Complexity:** Time = number of states · transitions; floating point (or fractions).

| # | Problem | Difficulty | Core idea |
|---|---------|:----------:|-----------|
| 688 | [Knight Probability in Chessboard](https://leetcode.com/problems/knight-probability-in-chessboard/) | Medium | dp[step][r][c] sum knight move probabilities/8 |
| 799 | [Champagne Tower](https://leetcode.com/problems/champagne-tower/) | Medium | flow overflow to children cells |
| 808 | [Soup Servings](https://leetcode.com/problems/soup-servings/) | Medium | memo expected prob over servings |
| 837 | [New 21 Game](https://leetcode.com/problems/new-21-game/) | Medium | sliding-window probability sum |
| 1227 | [Airplane Seat Assignment Probability](https://leetcode.com/problems/airplane-seat-assignment-probability/) | Medium | probability nth passenger correct seat |
| 1230 | [Toss Strange Coins](https://leetcode.com/problems/toss-strange-coins/) | Medium | dp[i][h] probability of h heads |
| 1467 | [Probability of a Two Boxes Having The Same Number of Distinct Balls](https://leetcode.com/problems/probability-of-a-two-boxes-having-the-same-number-of-distinct-balls/) | Hard | count balanced distributions probability |
| 1553 | [Minimum Number of Days to Eat N Oranges](https://leetcode.com/problems/minimum-number-of-days-to-eat-n-oranges/) | Hard | memo min days via n mod 2/3 divides |

---

## Other DP

**20 problems.** Problems whose DP doesn't fit a single clean archetype — hybrid states, ad-hoc recurrences, or DP used as a sub-step of a larger algorithm.

- **Recognize it when:** Mixed / unusual state design; treat case-by-case.
- **Recurrence:** Varies.
- **Complexity:** Varies.

| # | Problem | Difficulty | Core idea |
|---|---------|:----------:|-----------|
| 792 | [Number of Matching Subsequences](https://leetcode.com/problems/number-of-matching-subsequences/) | Medium | bucket words by next-needed char, advance |
| 907 | [Sum of Subarray Minimums](https://leetcode.com/problems/sum-of-subarray-minimums/) | Medium | monotonic stack contribution of minimums |
| 1182 | [Shortest Distance to Target Color](https://leetcode.com/problems/shortest-distance-to-target-color/) | Medium | precompute nearest color distance both directions |
| 1387 | [Sort Integers by The Power Value](https://leetcode.com/problems/sort-integers-by-the-power-value/) | Medium | memoize collatz power values, sort |
| 2439 | [Minimize Maximum of Array](https://leetcode.com/problems/minimize-maximum-of-array/) | Medium | binary search / prefix feasibility (not classic DP) |
| 2708 | [Maximum Strength of a Group](https://leetcode.com/problems/maximum-strength-of-a-group/) | Medium | track max/min product greedily |
| 2745 | [Construct the Longest New String](https://leetcode.com/problems/construct-the-longest-new-string/) | Medium | greedy/DP concatenating AA BB AB strings |
| 2998 | [Minimum Number of Operations to Make X and Y Equal](https://leetcode.com/problems/minimum-number-of-operations-to-make-x-and-y-equal/) | Medium | BFS/DP min ops divide/inc/dec |
| 3747 | [Count Distinct Integers After Removing Zeros](https://leetcode.com/problems/count-distinct-integers-after-removing-zeros/) | Medium | digit/string transform count |
| 42 | [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | Hard | left/right max prefix arrays for water |
| 410 | [Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) | Hard | binary search on max sum / interval dp |
| 458 | [Poor Pigs](https://leetcode.com/problems/poor-pigs/) | Hard | info-theoretic base=tests+1 encoding |
| 466 | [Count The Repetitions](https://leetcode.com/problems/count-the-repetitions/) | Hard | cycle detection of s1 matches per s2 block |
| 964 | [Least Operators to Express Number](https://leetcode.com/problems/least-operators-to-express-number/) | Hard | recursive base-x cost with memo on remainder |
| 1483 | [Kth Ancestor of a Tree Node](https://leetcode.com/problems/kth-ancestor-of-a-tree-node/) | Hard | binary lifting ancestor table |
| 1611 | [Minimum One Bit Operations to Make Integers Zero](https://leetcode.com/problems/minimum-one-bit-operations-to-make-integers-zero/) | Hard | gray-code recurrence f(2^k)=2^(k+1)-1 |
| 1714 | [Sum Of Special Evenly-Spaced Elements In Array](https://leetcode.com/problems/sum-of-special-evenly-spaced-elements-in-array/) | Hard | suffix sums grouped by step size |
| 2573 | [Find the String with LCP](https://leetcode.com/problems/find-the-string-with-lcp/) | Hard | reconstruct string from LCP via greedy/union |
| 2836 | [Maximize Value of Function in a Ball Passing Game](https://leetcode.com/problems/maximize-value-of-function-in-a-ball-passing-game/) | Hard | binary lifting on functional graph |
| 2851 | [String Transformation](https://leetcode.com/problems/string-transformation/) | Hard | matrix-power counting of rotations |

---
