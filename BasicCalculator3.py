#772. Basic Calculator III
class Solution:
    def calculate(self, s: str) -> int:
        def update(op, num):
            if op == '+':
                stack.append(num)
            elif op == '-':
                stack.append(-num)
            elif op == '*':
                stack.append(stack.pop() * num)
            elif op == '/':
                stack.append(int(stack.pop() / num))
                
        stack = []
        op = '+'
        num  = 0
        opset = set('+-/*')
        
        for c in s:
            if c.isdigit():
                num = num*10 + int(c)
            elif c in opset or c == ')':
                update(op,num)
                num = 0
                op = c
                if c == ')':
                    tmp_num = 0
                    while stack[-1] not in opset:
                        tmp_num += stack.pop()
                    update(stack.pop(),tmp_num)
            elif c == '(':
                stack.append(op)
                num = 0
                op  = '+'
        update(op,num)
        return sum(stack)
        
