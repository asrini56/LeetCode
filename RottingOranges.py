#994. Rotting Oranges, Time - O(N)
class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        queue = deque()
        fresh = 0
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == 2:
                    queue.append((i,j))
                elif grid[i][j] == 1:
                    fresh+=1
        queue.append((-1,-1))
        m = -1
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        while queue:
            r,c = queue.popleft()
            if r == -1:
                m += 1
                if queue:
                    queue.append((-1, -1))
            else:
                for d in directions:
                    r1 = r + d[0]
                    c1 = c + d[1]
                    if r1 >= 0 and r1 < len(grid) and c1 >= 0 and c1 < len(grid[r]):
                        if grid[r1][c1] == 1:
                            grid[r1][c1] = 2
                            fresh-=1
                            queue.append((r1,c1))
        if fresh == 0:
            return m
        else:
            return -1
