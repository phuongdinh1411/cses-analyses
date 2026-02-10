# Problem from UVA 12207 - That is Your Queue
# https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=3359
#
# Problem: Universal health care queue system
#
# Every citizen is assigned a unique number from 1 to P. They are put into a queue
# (1 in front of 2, 2 in front of 3, etc.). The hospital processes patients one by one.
# After being admitted, a citizen moves from front to back of the queue.
#
# Commands:
# - 'N': Next citizen is admitted (output their number, then they go to back)
# - 'E x': Expedite citizen x to the front of the queue
#
# Input:
# - Multiple test cases, each starting with P C (population, number of commands)
# - Next C lines: commands ('N' or 'E x')
# - Terminated by "0 0"
#
# Output: For each 'N' command, output which citizen is processed
#
# Approach: Use a linked list for efficient operations. Only track the first
#           min(P, C) citizens since we can't have more than C operations.


class Node:
    def __init__(self, data_val=None):
        self.data_val = data_val
        self.next_node = None


class MyLinkedList:
    def __init__(self):
        self.head_node = None
        self.tail_node = self.head_node

    def add_node(self, value=None):
        new_node = Node(value)
        if self.tail_node is not None:
            self.tail_node.next_node = new_node
            self.tail_node = new_node
        else:
            self.head_node = new_node
            self.tail_node = new_node

    def remove_head(self):
        head_value = self.head_node.data_val
        if self.head_node == self.tail_node:
            self.head_node = None
            self.tail_node = None
        else:
            self.head_node = self.head_node.next_node
        return head_value

    def remove_node(self, val_to_remove):
        cur_node = self.head_node
        cur_pre_node = None
        while cur_node is not None:
            if cur_node.data_val == val_to_remove:
                if cur_pre_node is not None:
                    cur_pre_node.next_node = cur_node.next_node
                else:
                    self.head_node = cur_node.next_node
                if cur_node.next_node is None:
                    self.tail_node = cur_pre_node
                return
            cur_pre_node = cur_node
            cur_node = cur_node.next_node

    def add_head(self, val_to_add):
        new_node = Node(val_to_add)
        if self.head_node is not None:
            new_node.next_node = self.head_node
            self.head_node = new_node
        else:
            self.head_node = new_node
            self.tail_node = new_node


results = []
while True:
    P, C = map(int, input().split())

    if P == 0:
        break
    P = min(P, C)

    cur_queue = MyLinkedList()
    for i in range(P):
        cur_queue.add_node(i + 1)
    cur_result = []
    for i in range(C):
        Ci = input()
        # Fixed: Use == instead of 'is' for string comparison
        if Ci == 'N':
            cur_treating = cur_queue.remove_head()
            cur_result.append(cur_treating)
            cur_queue.add_node(cur_treating)
        else:
            expedited_index = int(Ci.split()[1])
            cur_queue.remove_node(expedited_index)
            cur_queue.add_head(expedited_index)

    results.append(cur_result)

for i in range(len(results)):
    print('Case %d:' % (i + 1))
    print(*results[i], sep='\n')
