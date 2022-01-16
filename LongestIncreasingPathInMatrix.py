#Time/Space - O(mn)
class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        if not matrix or not matrix[0]:
            return 0

        # initilization
        M, N = len(matrix), len(matrix[0]) # length, width
        dp = [[0]*N for i in range(M)] # 2-D matrix for store the number of steps

        # dfs function
        def dfs(i, j):
            if not dp[i][j]: # if this position is not visited
                val = matrix[i][j]
                # search four directions to find out the decreasing path
                # up
                if i and val > matrix[i-1][j]:
                    up = dfs(i-1, j)
                else:
                    up = 0
                # down
                if i < M-1 and val > matrix[i+1][j]:
                    down = dfs(i+1, j)
                else:
                    down = 0
                # left
                if j and val > matrix[i][j-1]:
                    left = dfs(i, j-1)
                else:
                    left = 0
                # right
                if j < N-1 and val > matrix[i][j+1]:
                    right = dfs(i, j+1)
                else:
                    right = 0
                # "walk" to the target neighbor and accumulate the number of steps
                dp[i][j] = 1 + max(up, down, left, right)
            return dp[i][j]

        res_path = []
        for x in range(M): # search the grid by dfs
            for y in range(N):
                res_path.append(dfs(x, y))

        return max(res_path)
        
