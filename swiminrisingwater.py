"""
Input: grid = [[0,2],[1,3]]
Output: 3
Explanation:
At time 0, you are in grid location (0, 0).
You cannot go anywhere else because 4-directionally adjacent neighbors have a higher elevation than t = 0.
You cannot reach point (1, 1) until time 3.
When the depth of water is 3, we can swim anywhere inside the grid.

time - $O(V log V)$, where $V$ is the total number of cells in the grid

"""
class Solution:
    def swimInWater(self, grid: list[list[int]]) -> int:
        if not grid:
            return 0
        queue = [[grid[0][0],0,0]]
        visited = set()
        directions = [(0,1),(1,0),(0,-1),(-1,0)]
        n = len(grid)
        m = len(grid[0])

        while queue:
            time,row,col = heapq.heappop(queue)

            if row == n -1 and col == m - 1:
                return time
            
            if (row,col) in visited:
                continue
            
            visited.add((row,col))

            for d1,d2 in directions:
                nr = row + d1
                nc = col + d2

                if nr >= 0 and nr < n and nc >= 0 and nc < m and (nr,nc) not in visited:
                    heapq.heappush(queue, [max(time,grid[nr][nc]), nr, nc])
        
        return -1
