#227. Basic Calculator II, Time - O(n)
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
            elif c in opset:
                update(op,num)
                num = 0
                op  = c
        update(op,num)
        return sum(stack)
