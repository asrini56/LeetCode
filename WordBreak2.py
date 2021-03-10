class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
        dp = {}
        def word(s):
            if s in dp:
                return dp[s]
            res = []
            for i in wordDict:
                if s[:len(i)] == i:
                    if len(i) == len(s):
                        res.append(i)
                    else:
                        tmp = word(s[len(i):])
                        for t in tmp:
                            res.append(i + " " + t)
            dp[s] = res
            return res
        return word(s)
                    
