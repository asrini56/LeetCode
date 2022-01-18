class Solution:
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        n = len(grid)
        if grid[0][0] == 1 or grid[n-1][n-1] == 1:
            return -1
        moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        queue = collections.deque([(0,0,1)])
        seen = {(0,0)}
        while queue:
            i,j,d = queue.popleft()
            if i == j == n - 1:
                return d
            else:
                for d1,d2 in moves:
                    r = i + d1
                    c = j + d2
                    if (r,c) not in seen and 0 <= r < n and c >= 0 and c < n and grid[r][c] == 0:
                        queue.append((r,c,d+1))
                        seen.add((r,c))
        return -1
