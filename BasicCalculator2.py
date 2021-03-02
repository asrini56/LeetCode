#227. Basic Calculator II, Time - O(n)
class Solution:
    def calculate(self, s: str) -> int:
        stack = []
        curr = 0
        currop = '+'
        for i in range(len(s)):
            char = s[i]
            if char.isdigit():
                curr = (curr*10) + int(char)
            if char.isdigit() == False and not char.isspace() or i == len(s) - 1:
                if currop == '+':
                    stack.append(curr)
                elif currop == '-':
                    stack.append(-curr)
                elif currop == '*':
                    c = stack.pop()
                    stack.append(c*curr)
                elif currop == '/':
                    c = stack.pop()
                    stack.append(int(c/curr))
                currop = char
                curr = 0
        result = 0
        while stack:
            result+=stack.pop()
        return result
