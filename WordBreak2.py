"""
Let N be the length of the input string and W be the number of words in the dictionary.
Time Complexity: O(N ^ 2 + 2^N + W)
"""
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
        memo = {}
        def dfs(s):
            if s in memo:
                return memo[s]
            res = []
            for x in wordDict:
                if s.startswith(x):
                    if s == x:
                        res += [x]
                    else:
                        for y in dfs(s[len(x):]):
                            res += [x + ' ' + y]
            memo[s] = res
            return res             
        return dfs(s)
                    
