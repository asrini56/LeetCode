#14. Longest Common Prefix, Time - O(S)
class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if len(strs) == 0:
            return ""
        p = str(strs[0])
        for i in range(len(strs)):
            j = len(p)
            while(j >= 0):
                if strs[i].startswith(p):
                    j = -1
                else:
                    p = p[:j-1]
                    j = j - 1
            if p == "":
                return ""
        return p
