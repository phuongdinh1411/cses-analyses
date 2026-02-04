---
layout: simple
title: "Session 05 - String"
permalink: /problem_soulutions/Blue/Session 05 - String/
---

# Session 05 - String

This session covers string manipulation, pattern matching, and text processing algorithms.

## Problems

### 43A (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/43/A

# One day Vasya decided to have a look at the results of Berland 1910 Football Championship’s finals. Unfortunately he didn't find the overall score of the match; however, he got hold of a profound description of the match's process. On the whole there are n lines in that description each of which described one goal. Every goal was marked with the name of the team that had scored it. Help Vasya, learn the name of the team that won the finals. It is guaranteed that the match did not end in a tie.
#
# Input
# The first line contains an integer n (1 ≤ n ≤ 100) — the number of lines in the description. Then follow n lines — for each goal the names of the teams that scored it. The names are non-empty lines consisting of uppercase Latin letters whose lengths do not exceed 10 symbols. It is guaranteed that the match did not end in a tie and the description contains no more than two different teams.
#
# Output
# Print the name of the winning team. We remind you that in football the team that scores more goals is considered the winner.
#
# Examples
# input
# 1
# ABC
# output
# ABC
# input
# 5
# A
# ABA
# ABA
# A
# A
# output
# A

n = int(input())
result = {}
first_team = input().strip()
first_team_score = 1
second_team = ''
for i in range(1, n):
    cur_team_score = input().strip()
    if cur_team_score != first_team:
        first_team_score -= 1
        second_team = cur_team_score
    else:
        first_team_score += 1

print(first_team if first_team_score > 0 else second_team)
```

### 448B (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/448/B

# Bizon the Champion isn't just a bison. He also is a favorite of the "Bizons" team.
#
# At a competition the "Bizons" got the following problem: "You are given two distinct words (strings of English letters), s and t. You need to transform word s into word t". The task looked simple to the guys because they know the suffix data structures well. Bizon Senior loves suffix automaton. By applying it once to a string, he can remove from this string any single character. Bizon Middle knows suffix array well. By applying it once to a string, he can swap any two characters of this string. The guys do not know anything about the suffix tree, but it can help them do much more.
#
# Bizon the Champion wonders whether the "Bizons" can solve the problem. Perhaps, the solution do not require both data structures. Find out whether the guys can solve the problem and if they can, how do they do it? Can they solve it either only with use of suffix automaton or only with use of suffix array or they need both structures? Note that any structure may be used an unlimited number of times, the structures may be used in any order.
#
# Input
# The first line contains a non-empty word s. The second line contains a non-empty word t. Words s and t are different. Each word consists only of lowercase English letters. Each word contains at most 100 letters.
#
# Output
# In the single line print the answer to the problem. Print "need tree" (without the quotes) if word s cannot be transformed into word t even with use of both suffix array and suffix automaton. Print "automaton" (without the quotes) if you need only the suffix automaton to solve the problem. Print "array" (without the quotes) if you need only the suffix array to solve the problem. Print "both" (without the quotes), if you need both data structures to solve the problem.
#
# It's guaranteed that if you can solve the problem only with use of suffix array, then it is impossible to solve it only with use of suffix automaton. This is also true for suffix automaton.
#
# Examples
# input
# automaton
# tomat
# output
# automaton
# input
# array
# arary
# output
# array
# input
# both
# hot
# output
# both
# input
# need
# tree
# output
# need tree
# Note
# In the third sample you can act like that: first transform "both" into "oth" by removing the first character using the suffix automaton and then make two swaps of the string using the suffix array and get "hot".


def check_solution(_s, _t):
    is_array = False

    s_map = [0] * 26
    t_map = [0] * 26

    s_length = len(_s)
    t_length = len(_t)

    for i in range(s_length):
        s_map[ord(_s[i]) - 97] += 1

    for i in range(t_length):
        t_map[ord(_t[i]) - 97] += 1

    for i in range(26):
        if s_map[i] < t_map[i]:
            return 'need tree'

    if s_length == t_length:
        return 'array'

    s_left = 0
    t_left = 0
    while True:
        if s_left >= s_length or t_left >= t_length:
            break
        if _s[s_left] != _t[t_left]:
            s_left += 1
        else:
            s_left += 1
            t_left += 1
        if s_length - s_left < t_length - t_left:
            is_array = True
            break

    if is_array:
        return 'both'

    return 'automaton'


s = input()
t = input()

print(check_solution(s, t))
```

### 499B (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/499/B

# You have a new professor of graph theory and he speaks very quickly. You come up with the following plan to keep up with his lecture and make notes.
#
# You know two languages, and the professor is giving the lecture in the first one. The words in both languages consist of lowercase English characters, each language consists of several words. For each language, all words are distinct, i.e. they are spelled differently. Moreover, the words of these languages have a one-to-one correspondence, that is, for each word in each language, there exists exactly one word in the other language having has the same meaning.
#
# You can write down every word the professor says in either the first language or the second language. Of course, during the lecture you write down each word in the language in which the word is shorter. In case of equal lengths of the corresponding words you prefer the word of the first language.
#
# You are given the text of the lecture the professor is going to read. Find out how the lecture will be recorded in your notes.
#
# Input
# The first line contains two integers, n and m (1 ≤ n ≤ 3000, 1 ≤ m ≤ 3000) — the number of words in the professor's lecture and the number of words in each of these languages.
#
# The following m lines contain the words. The i-th line contains two strings ai, bi meaning that the word ai belongs to the first language, the word bi belongs to the second language, and these two words have the same meaning. It is guaranteed that no word occurs in both languages, and each word occurs in its language exactly once.
#
# The next line contains n space-separated strings c1, c2, ..., cn — the text of the lecture. It is guaranteed that each of the strings ci belongs to the set of strings {a1, a2, ... am}.
#
# All the strings in the input are non-empty, each consisting of no more than 10 lowercase English letters.
#
# Output
# Output exactly n words: how you will record the lecture in your notebook. Output the words of the lecture in the same order as in the input.
#
# Examples
# input
# 4 3
# codeforces codesecrof
# contest round
# letter message
# codeforces contest letter contest
# output
# codeforces round letter round
# input
# 5 3
# joll wuqrd
# euzf un
# hbnyiyc rsoqqveh
# hbnyiyc joll joll euzf joll
# output
# hbnyiyc joll joll un joll


def get_shorter(ci, _a, _b):
    _i = 0
    while ci != _a[_i]:
        _i += 1

    return _a[_i] if len(_a[_i]) <= len(_b[_i]) else _b[_i]


n, m = map(int, input().split())
a = []
b = []
for i in range(m):
    ai, bi = input().split()
    a.append(ai)
    b.append(bi)
c = input().split()

result = []

for i in range(n):
    result.append(get_shorter(c[i], a, b))

print(*result, sep=' ')
```

### 518A (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/518/A

# Vitaly is a diligent student who never missed a lesson in his five years of studying in the university. He always does his homework on time and passes his exams in time.
#
# During the last lesson the teacher has provided two strings s and t to Vitaly. The strings have the same length, they consist of lowercase English letters, string s is lexicographically smaller than string t. Vitaly wondered if there is such string that is lexicographically larger than string s and at the same is lexicographically smaller than string t. This string should also consist of lowercase English letters and have the length equal to the lengths of strings s and t.
#
# Let's help Vitaly solve this easy problem!
#
# Input
# The first line contains string s (1 ≤ |s| ≤ 100), consisting of lowercase English letters. Here, |s| denotes the length of the string.
#
# The second line contains string t (|t| = |s|), consisting of lowercase English letters.
#
# It is guaranteed that the lengths of strings s and t are the same and string s is lexicographically less than string t.
#
# Output
# If the string that meets the given requirements doesn't exist, print a single string "No such string" (without the quotes).
#
# If such string exists, print it. If there are multiple valid strings, you may print any of them.
#
# Examples
# input
# a
# c
# output
# b
# input
# aaa
# zzz
# output
# kkk
# input
# abcdefg
# abcdefh
# output
# No such string
# Note
# String s = s1s2... sn is said to be lexicographically smaller than t = t1t2... tn, if there exists such i, that s1 = t1, s2 = t2, ... si - 1 = ti - 1, si < ti.

s = input().strip()
t = input().strip()
first_smaller = -1
result = 'No such string'
for i in range(len(s)):
    if ord(t[i]) - ord(s[i]) >= 2:
        result = s[:i] + chr(ord(s[i]) + 1) + s[i + 1:]
        break
    if ord(t[i]) > ord(s[i]):
        first_smaller = i
        break

if first_smaller >= 0:
    if s[first_smaller + 1:] >= t[first_smaller + 1:]:
        for i in range(first_smaller + 1, len(t)):
            if t[i] is not 'a':
                result = s[:first_smaller] + chr(ord(s[first_smaller]) + 1) + t[first_smaller + 1:i] + chr(
                    ord(t[i]) - 1) + t[i + 1:]
                break
            if s[i] is not 'z':
                result = s[:i] + chr(ord(s[i]) + 1) + s[i + 1:]
                break
    elif s[first_smaller + 1:] < t[first_smaller + 1:]:
        result = s[:first_smaller] + chr(ord(s[first_smaller]) + 1) + s[first_smaller + 1:]

print(result)


#  New solution: +1 for s
```

### 518B (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/518/B

# Little Tanya decided to present her dad a postcard on his Birthday. She has already created a message — string s of length n, consisting of uppercase and lowercase English letters. Tanya can't write yet, so she found a newspaper and decided to cut out the letters and glue them into the postcard to achieve string s. The newspaper contains string t, consisting of uppercase and lowercase English letters. We know that the length of string t greater or equal to the length of the string s.
#
# The newspaper may possibly have too few of some letters needed to make the text and too many of some other letters. That's why Tanya wants to cut some n letters out of the newspaper and make a message of length exactly n, so that it looked as much as possible like s. If the letter in some position has correct value and correct letter case (in the string s and in the string that Tanya will make), then she shouts joyfully "YAY!", and if the letter in the given position has only the correct value but it is in the wrong case, then the girl says "WHOOPS".
#
# Tanya wants to make such message that lets her shout "YAY!" as much as possible. If there are multiple ways to do this, then her second priority is to maximize the number of times she says "WHOOPS". Your task is to help Tanya make the message.
#
# Input
# The first line contains line s (1 ≤ |s| ≤ 2·105), consisting of uppercase and lowercase English letters — the text of Tanya's message.
#
# The second line contains line t (|s| ≤ |t| ≤ 2·105), consisting of uppercase and lowercase English letters — the text written in the newspaper.
#
# Here |a| means the length of the string a.
#
# Output
# Print two integers separated by a space:
#
# the first number is the number of times Tanya shouts "YAY!" while making the message,
# the second number is the number of times Tanya says "WHOOPS" while making the message.
# Examples
# input
# AbC
# DCbA
# output
# 3 0
# input
# ABC
# abc
# output
# 0 3
# input
# abacaba
# AbaCaBA
# output
# 3 4

s = input().strip()
t = input().strip()

yay = 0
whoops = 0

yay_map = [0] * 58
whoops_map = [] * 58

slength = len(s)
tlength = len(t)

s_map = [0] * 58
t_map = [0] * 58
up_low_distance = 32

for i in range(slength):
    s_map[ord(s[i]) - 65] += 1

for i in range(tlength):
    t_map[ord(t[i]) - 65] += 1

for i in range(26):
    # Go with YAY!
    if t_map[i] >= s_map[i]:
        yay += s_map[i]
        t_map[i] -= s_map[i]
        s_map[i] = 0
    else:
        yay += t_map[i]
        s_map[i] -= t_map[i]
        t_map[i] = 0

    if t_map[i + up_low_distance] >= s_map[i + up_low_distance]:
        yay += s_map[i + up_low_distance]
        t_map[i + up_low_distance] -= s_map[i + up_low_distance]
        s_map[i + up_low_distance] = 0
    else:
        yay += t_map[i + up_low_distance]
        s_map[i + up_low_distance] -= t_map[i + up_low_distance]
        t_map[i + up_low_distance] = 0

    # Go with WHOOPS
    if t_map[i] >= s_map[i + up_low_distance]:
        whoops += s_map[i + up_low_distance]
        t_map[i] -= s_map[i + up_low_distance]
        s_map[i + up_low_distance] = 0
    else:
        whoops += t_map[i]
        s_map[i + up_low_distance] -= t_map[i]
        t_map[i] = 0

    if t_map[i + up_low_distance] >= s_map[i]:
        whoops += s_map[i]
        t_map[i + up_low_distance] -= s_map[i]
        s_map[i] = 0
    else:
        whoops += t_map[i + up_low_distance]
        s_map[i] -= t_map[i + up_low_distance]
        t_map[i + up_low_distance] = 0

print(yay, whoops)
```

### 61B (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/61/B

# After the contest in comparing numbers, Shapur's teacher found out that he is a real genius and that no one could possibly do the calculations faster than him even using a super computer!
#
# Some days before the contest, the teacher took a very simple-looking exam and all his n students took part in the exam. The teacher gave them 3 strings and asked them to concatenate them. Concatenating strings means to put them in some arbitrary order one after the other. For example from concatenating Alireza and Amir we can get to AlirezaAmir or AmirAlireza depending on the order of concatenation.
#
# Unfortunately enough, the teacher forgot to ask students to concatenate their strings in a pre-defined order so each student did it the way he/she liked.
#
# Now the teacher knows that Shapur is such a fast-calculating genius boy and asks him to correct the students' papers.
#
# Shapur is not good at doing such a time-taking task. He rather likes to finish up with it as soon as possible and take his time to solve 3-SAT in polynomial time. Moreover, the teacher has given some advice that Shapur has to follow. Here's what the teacher said:
#
# As I expect you know, the strings I gave to my students (including you) contained only lowercase and uppercase Persian Mikhi-Script letters. These letters are too much like Latin letters, so to make your task much harder I converted all the initial strings and all of the students' answers to Latin.
# As latin alphabet has much less characters than Mikhi-Script, I added three odd-looking characters to the answers, these include "-", ";" and "_". These characters are my own invention of course! And I call them Signs.
# The length of all initial strings was less than or equal to 100 and the lengths of my students' answers are less than or equal to 600
# My son, not all students are genius as you are. It is quite possible that they make minor mistakes changing case of some characters. For example they may write ALiReZaAmIR instead of AlirezaAmir. Don't be picky and ignore these mistakes.
# Those signs which I previously talked to you about are not important. You can ignore them, since many students are in the mood for adding extra signs or forgetting about a sign. So something like Iran;;-- is the same as --;IRAN
# You should indicate for any of my students if his answer was right or wrong. Do this by writing "WA" for Wrong answer or "ACC" for a correct answer.
# I should remind you that none of the strings (initial strings or answers) are empty.
# Finally, do these as soon as possible. You have less than 2 hours to complete this.
# Input
# The first three lines contain a string each. These are the initial strings. They consists only of lowercase and uppercase Latin letters and signs ("-", ";" and "_"). All the initial strings have length from 1 to 100, inclusively.
#
# In the fourth line there is a single integer n (0 ≤ n ≤ 1000), the number of students.
#
# Next n lines contain a student's answer each. It is guaranteed that the answer meets what the teacher said. Each answer iconsists only of lowercase and uppercase Latin letters and signs ("-", ";" and "_"). Length is from 1 to 600, inclusively.
#
# Output
# For each student write in a different line. Print "WA" if his answer is wrong or "ACC" if his answer is OK.
#
# Examples
# input
# Iran_
# Persian;
# W_o;n;d;e;r;f;u;l;
# 7
# WonderfulPersianIran
# wonderful_PersIAN_IRAN;;_
# WONDERFUL___IRAN__PERSIAN__;;
# Ira__Persiann__Wonderful
# Wonder;;fulPersian___;I;r;a;n;
# __________IranPersianWonderful__________
# PersianIran_is_Wonderful
# output
# ACC
# ACC
# ACC
# WA
# ACC
# ACC
# WA
# input
# Shapur;;
# is___
# a_genius
# 3
# Shapur__a_is___geniUs
# is___shapur___a__Genius;
# Shapur;;is;;a;;geni;;us;;
# output
# WA
# ACC
# ACC

str11 = input().strip().replace(';', '').replace('-', '').replace('_', '').lower()
str12 = input().strip().replace(';', '').replace('-', '').replace('_', '').lower()
str13 = input().strip().replace(';', '').replace('-', '').replace('_', '').lower()

n = int(input())
for i in range(n):
    ai = input().strip().replace(';', '').replace('-', '').replace('_', '').lower()
    if len(ai) != len(str11) + len(str12) + len(str13):
        print('WA')
        continue
    if (str11 + str12 + str13) == ai or (str11 + str13 + str12) == ai or (str12 + str11 + str13) == ai or (
            str12 + str13 + str11) == ai or (str13 + str11 + str12) == ai or (str13 + str12 + str11) == ai:
        print('ACC')
        continue
    print('WA')
```

### 721B (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/721/B

# Vanya is managed to enter his favourite site Codehorses. Vanya uses n distinct passwords for sites at all, however he can't remember which one exactly he specified during Codehorses registration.
#
# Vanya will enter passwords in order of non-decreasing their lengths, and he will enter passwords of same length in arbitrary order. Just when Vanya will have entered the correct password, he is immediately authorized on the site. Vanya will not enter any password twice.
#
# Entering any passwords takes one second for Vanya. But if Vanya will enter wrong password k times, then he is able to make the next try only 5 seconds after that. Vanya makes each try immediately, that is, at each moment when Vanya is able to enter password, he is doing that.
#
# Determine how many seconds will Vanya need to enter Codehorses in the best case for him (if he spends minimum possible number of second) and in the worst case (if he spends maximum possible amount of seconds).
#
# Input
# The first line of the input contains two integers n and k (1 ≤ n, k ≤ 100) — the number of Vanya's passwords and the number of failed tries, after which the access to the site is blocked for 5 seconds.
#
# The next n lines contains passwords, one per line — pairwise distinct non-empty strings consisting of latin letters and digits. Each password length does not exceed 100 characters.
#
# The last line of the input contains the Vanya's Codehorses password. It is guaranteed that the Vanya's Codehorses password is equal to some of his n passwords.
#
# Output
# Print two integers — time (in seconds), Vanya needs to be authorized to Codehorses in the best case for him and in the worst case respectively.
#
# Examples
# input
# 5 2
# cba
# abc
# bb1
# abC
# ABC
# abc
# output
# 1 15
# input
# 4 100
# 11
# 22
# 1
# 2
# 22
# output
# 3 4
# Note
# Consider the first sample case. As soon as all passwords have the same length, Vanya can enter the right password at the first try as well as at the last try. If he enters it at the first try, he spends exactly 1 second. Thus in the best case the answer is 1. If, at the other hand, he enters it at the last try, he enters another 4 passwords before. He spends 2 seconds to enter first 2 passwords, then he waits 5 seconds as soon as he made 2 wrong tries. Then he spends 2 more seconds to enter 2 wrong passwords, again waits 5 seconds and, finally, enters the correct password spending 1 more second. In summary in the worst case he is able to be authorized in 15 seconds.
#
# Consider the second sample case. There is no way of entering passwords and get the access to the site blocked. As soon as the required password has length of 2, Vanya enters all passwords of length 1 anyway, spending 2 seconds for that. Then, in the best case, he immediately enters the correct password and the answer for the best case is 3, but in the worst case he enters wrong password of length 2 and only then the right one, spending 4 seconds at all.


n, k = map(int, input().split())

passwords = []
for i in range(n):
    passwords.append(input())

passwords = sorted(passwords, key=lambda x: -len(x))
correct_pwd = input()
right_break_point = n - 1
left_break_point = 0
for i in range(n - 1, -1, -1):
    if len(correct_pwd) == len(passwords[i]):
        right_break_point = i
        break

for i in range(right_break_point, -1, -1):
    if len(correct_pwd) != len(passwords[i]):
        left_break_point = i + 1
        break

same_length_list = passwords[left_break_point:right_break_point + 1]

number_of_corrects = 0
for i in range(len(same_length_list)):
    if same_length_list[i] == correct_pwd:
        number_of_corrects += 1

counter_best_case = n - right_break_point
counter_worst_case = n - (left_break_point + number_of_corrects - 1)
best_case_mod = 1 if counter_best_case % k == 0 and counter_best_case // k > 0 else 0
worst_case_mod = 1 if counter_worst_case % k == 0 and counter_worst_case // k > 0 else 0
best_case = counter_best_case + (counter_best_case // k - best_case_mod) * 5
worst_case = counter_worst_case + (counter_worst_case // k - worst_case_mod) * 5

print(best_case, worst_case)
```

### 731A (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/731/A

# Grigoriy, like the hero of one famous comedy film, found a job as a night security guard at the museum. At first night he received embosser and was to take stock of the whole exposition.
# 
# Embosser is a special devise that allows to "print" the text of a plastic tape. Text is printed sequentially, character by character. The device consists of a wheel with a lowercase English letters written in a circle, static pointer to the current letter and a button that print the chosen letter. At one move it's allowed to rotate the alphabetic wheel one step clockwise or counterclockwise. Initially, static pointer points to letter 'a'. Other letters are located as shown on the picture:
# 
# 
# After Grigoriy add new item to the base he has to print its name on the plastic tape and attach it to the corresponding exhibit. It's not required to return the wheel to its initial position with pointer on the letter 'a'.
# 
# Our hero is afraid that some exhibits may become alive and start to attack him, so he wants to print the names as fast as possible. Help him, for the given string find the minimum number of rotations of the wheel required to print it.
# 
# Input
# The only line of input contains the name of some exhibit — the non-empty string consisting of no more than 100 characters. It's guaranteed that the string consists of only lowercase English letters.
# 
# Output
# Print one integer — the minimum number of rotations of the wheel, required to print the name given in the input.
# 
# Examples
# input
# zeus
# output
# 18
# input
# map
# output
# 35
# input
# ares
# output
# 34

ex_name = input()
result = 0
# 97 = a, 122 = z
cur_pos = 97
for c in ex_name:
    result += min(abs(ord(c) - cur_pos), 26 - abs(ord(c) - cur_pos))
    cur_pos = ord(c)
print(result)
```

### 90B (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/90/B

# An African crossword is a rectangular table n × m in size. Each cell of the table contains exactly one letter. This table (it is also referred to as grid) contains some encrypted word that needs to be decoded.
#
# To solve the crossword you should cross out all repeated letters in rows and columns. In other words, a letter should only be crossed out if and only if the corresponding column or row contains at least one more letter that is exactly the same. Besides, all such letters are crossed out simultaneously.
#
# When all repeated letters have been crossed out, we should write the remaining letters in a string. The letters that occupy a higher position follow before the letters that occupy a lower position. If the letters are located in one row, then the letter to the left goes first. The resulting word is the answer to the problem.
#
# You are suggested to solve an African crossword and print the word encrypted there.
#
# Input
# The first line contains two integers n and m (1 ≤ n, m ≤ 100). Next n lines contain m lowercase Latin letters each. That is the crossword grid.
#
# Output
# Print the encrypted word on a single line. It is guaranteed that the answer consists of at least one letter.
#
# Examples
# input
# 3 3
# cba
# bcd
# cbc
# output
# abcd
# input
# 5 5
# fcofd
# ooedo
# afaoa
# rdcdf
# eofsf
# output
# codeforces


n, m = map(int, input().split())
rectangular = []
result = ''

matrix = [[0 for i in range(m)] for j in range(n)]

for i in range(n):
    rectangular.append(input())

for i in range(n):
    for j in range(m):
        if matrix[i][j] == 0:  # not crossed yet
            for row_checker in range(m):
                if row_checker != j and rectangular[i][row_checker] == rectangular[i][j]:
                    matrix[i][row_checker] = 1
                    matrix[i][j] = 1
            for col_checker in range(n):
                if col_checker != i and rectangular[col_checker][j] == rectangular[i][j]:
                    matrix[col_checker][j] = 1
                    matrix[i][j] = 1


for i in range(n):
    for j in range(m):
        if matrix[i][j] == 0:
            result += rectangular[i][j]

print(result)
```

