#Time - O(m*n^3) - 3 direction traversal
class Solution:
    def uniquePathsIII(self, grid: List[List[int]]) -> int:
        
        m, n = len(grid), len(grid[0])
        # iterate through the grid to get relevant info
        start = None  # to store starting point
        count = 0  # to count number of squares to walk over
        self.ans = 0
        for i in range(m):
            for j in range(n):
                count += grid[i][j] == 0
                if not start and grid[i][j] == 1:
                    start = [i, j]
        
        def backtrack(i,j):
            nonlocal count
            for x, y in ((i-1, j), (i+1, j), (i, j-1), (i, j+1)):
                # border check
                if 0 <= x < m and 0 <= y < n:
                    if grid[x][y] == 0:
                        # traverse down this path
                        grid[x][y] = -1
                        count -= 1
                        # backtrack and reset
                        backtrack(x,y)
                        grid[x][y] = 0
                        count += 1
                    elif grid[x][y] == 2:
                        # check if all squares have been walked over
                        if count == 0:
                            self.ans+=1
        
        backtrack(start[0],start[1])
        return self.ans
