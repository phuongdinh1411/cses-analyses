# Problem from SPOJ
# https://www.spoj.com/problems/ONP/
#
# ONP - Transform the Expression
#
# Transform algebraic expression with brackets into RPN form (Reverse Polish Notation).
# Operators: +, -, *, /, ^ (priority from lowest to highest)
# Brackets: ( )
# Operands: only letters a-z
#
# Input:
# - t: number of expressions (<= 100)
# - t lines of expressions (length <= 400)
#
# Output: Expressions in RPN form, one per line
#
# Example:
# Input: (a+(b*c))
# Output: abc*+
#
# Approach: Shunting-yard algorithm
# - Operands go directly to output
# - Operators go to stack, pop higher/equal priority operators first
# - '(' goes to stack
# - ')' pops until '(' is found

n = int(input())
results = []

operator_priority = {
    '+': 1,
    '-': 2,
    '*': 3,
    '/': 4,
    '^': 5
}

for i in range(n):
    cur_exp = input()
    cur_output = ''
    operator_stack = []

    for char in cur_exp:
        char_priority = operator_priority.get(char)

        # Fixed: Use == and != instead of 'is' and 'is not' for string comparison
        if char_priority is None and char != ')' and char != '(':
            # This is an operand (letter)
            cur_output += char
        elif char_priority is not None:
            # This is an operator
            while (operator_stack and
                   operator_priority.get(operator_stack[-1]) is not None and
                   operator_priority.get(operator_stack[-1]) >= char_priority):
                cur_output += operator_stack.pop()
            operator_stack.append(char)
        elif char == '(':
            operator_stack.append(char)
        else:  # char == ')'
            while operator_stack:
                top = operator_stack.pop()
                if top == '(':
                    break
                cur_output += top

    # Pop remaining operators
    while operator_stack:
        top = operator_stack.pop()
        cur_output += top

    results.append(cur_output)

print(*results, sep='\n')
