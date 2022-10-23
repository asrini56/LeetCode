#576. Out of Boundary Paths, Time = O(m * n * maxMove) = O(n^3)
class Solution:
    def __init__(self):
        self.count = 0
    def findPaths(self, m: int, n: int, maxMove: int, startRow: int, startColumn: int) -> int:
        dp = [[[-1]*(maxMove+1) for _ in range(n+1)] for _ in range(m+1)]
        return self.dfs(startRow,startColumn,maxMove,m,n,dp) % 1000000007
    def dfs(self,row,col,maxMove,m,n,dp):
        if dp[row][col][maxMove] != -1:
            return dp[row][col][maxMove]
        else:
            if (row < 0 or col < 0 or row >= m or col >= n) and maxMove >= 0:
                return 1
            if not maxMove:
                return 0
            if maxMove:
                a = self.dfs(row-1,col,maxMove-1,m,n,dp)
                b = self.dfs(row+1,col,maxMove-1,m,n,dp)
                c = self.dfs(row,col-1,maxMove-1,m,n,dp)
                d = self.dfs(row,col+1,maxMove-1,m,n,dp)
                dp[row][col][maxMove] = a+b+c+d
                return dp[row][col][maxMove]
