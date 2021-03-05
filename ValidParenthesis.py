#20. Valid Parentheses, Time - O(n)
class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        m = {')':'(','}':'{',']':'['}
        for i in s:
            if i in m:
                if stack:
                    node = stack.pop()
                else:
                    node = '#'
                if m[i] != node:
                    return False
            else:
                stack.append(i)
        if stack:
            return False
        else:
            return True
