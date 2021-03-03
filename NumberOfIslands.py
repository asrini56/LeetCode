#200. Number of Islands
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        visited = set()
        def dfs(i,j,grid):
            if i < 0 or j < 0 or i >= len(grid) or j >= len(grid[0]):
                return
            if grid[i][j] == "1" and (i,j) not in visited:
                visited.add((i,j))
                dfs(i+1,j,grid)
                dfs(i-1,j,grid)
                dfs(i,j+1,grid)
                dfs(i,j-1,grid)
        res = 0
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == "1" and (i,j) not in visited:
                    res+=1
                    dfs(i,j,grid)
        return res
