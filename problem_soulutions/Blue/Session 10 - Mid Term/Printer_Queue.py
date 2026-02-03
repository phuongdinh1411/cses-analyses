# Problem: Printer Queue (UVA 12100)
#
# Problem Description:
# A printer queue processes jobs based on priority, not just FIFO order.
# Jobs with higher priority are printed first. If the front job doesn't have
# the highest priority, it's moved to the back of the queue.
# Find when a specific job (at position m) will be printed.
#
# Input Format:
# - T: number of test cases
# - For each test case:
#   - n m: number of jobs and position of our job (0-indexed)
#   - n integers: priorities of each job
#
# Output Format:
# - For each test case: the order in which our job is printed (1-indexed)
#
# Key Approach/Algorithm:
# - Simulate the printer queue using a list
# - Sort priorities in descending order to know which priority should print next
# - If front job has the current highest priority, print it; otherwise move to back
# - Track when our target job gets printed

def solution():
    tcs = int(input())
    for i in range(tcs):
        n, m = map(int, input().split())
        printer_queue = list(map(int, input().split()))
        sorted_list = sorted(printer_queue, reverse=True)
        counter = 0
        pointer = 0
        largest_pos = 0
        while True:
            if largest_pos >= n:
                break

            if printer_queue[pointer] == sorted_list[largest_pos]:
                counter += 1
                largest_pos += 1
                if pointer == m:
                    break
            else:
                if pointer == m:
                    m = len(printer_queue)
                printer_queue.append(printer_queue[pointer])

            pointer += 1

        print(counter)


solution()
