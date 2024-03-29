#Unique Paths, Time - O(n*m), Space - O(n*m)
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [[1]*n for i in range(m)]
        for i in range(1,m):
            for j in range(1,n):
                dp[i][j] = dp[i-1][j] + dp[i][j-1]
        return dp[m-1][n-1]

    
    
#Unique Paths, Time - O(n*m), Space - O(m)
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [1]*n
        for _, j in product(range(1, m), range(1, n)):
            dp[j] += dp[j-1]
        return dp[-1]
