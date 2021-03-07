#1143. Longest Common Subsequence, Time - O(m*n)
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        if not text1 or not text2:
            return 0
        m = len(text1)
        n = len(text2)
        dp = [[0]*(n+1) for i in range(m+1)]
        print(dp)
        for i in range(m+1):
            for j in range(n+1):
                if i == 0 or j == 0:
                    dp[i][j] = 0
                elif text1[i-1] == text2[j-1]:
                    dp[i][j] = dp[i-1][j-1]+1
                else:
                    dp[i][j] = max(dp[i-1][j],dp[i][j-1])
        return dp[m][n]
    
    """
    working:
        a c e
      0 0 0 0
    a 0 1 1 1
    b 0 1 1 1
    c 0 1 2 2
    d 0 1 2 2
    e 0 1 2 3
    
    ans = 3 [ace]
    """
