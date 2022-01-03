class Solution:
    def longestValidParentheses(self, s: str) -> int:
        s1 = list(s)
        stack = [-1]
        count = 0
        for i in range(len(s1)):
            if s1[i] == '(':
                stack.append(i)
            else:
                if stack:
                    stack.pop()
                if not stack:
                    stack.append(i)
                else:
                    count = max(count,i-stack[-1])
        return count
