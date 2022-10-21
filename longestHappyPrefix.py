#1392. Longest Happy Prefix - KMP Search , Time - O(n), Space - O(n)
class Solution:
    def longestPrefix(self, s: str) -> str:
        if not s:
            return ""
        ans = [0] * len(s)
        i = 1
        j = 0
        while i < len(s):
            if s[i] == s[j]:
                ans[i] = j + 1
                i+=1
                j+=1
            else:
                if j:
                    j = ans[j-1]
                else:
                    ans[i] = 0
                    i+=1
        return s[:ans[-1]]
