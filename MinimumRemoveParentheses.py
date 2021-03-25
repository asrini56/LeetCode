#1249. Minimum Remove to Make Valid Parentheses, Time - O(n)
class Solution:
    def minRemoveToMakeValid(self, s: str) -> str:
        index = set()
        st = []
        for i in range(len(s)):
            if s[i] != '(' and s[i] != ')':
                continue
            if s[i] == '(':
                st.append(i)
            elif not st:
                index.add(i)
            else:
                st.pop()
        while st:
            index.add(st.pop())
        ans = []
        for i in range(len(s)):
            if i not in index:
                ans.append(s[i])
        return ''.join(ans)
