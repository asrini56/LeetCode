class Solution:
    def shortestPath(self, grid: List[List[int]], k: int) -> int:
        m, n = len(grid), len(grid[0])
        if m * n <= 1:
            return 0
        visited = {(0, 0, k)}
        queue = collections.deque([(0, 0, k)])
        steps = 0
        while queue:
            size = len(queue)
            for _ in range(size):
                x, y, k = queue.popleft()
                for x1, y1 in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                    if 0 <= x1 < m and 0 <= y1 < n:
                        if x1 == m - 1 and y1 == n - 1:
                            return steps + 1
                        if grid[x1][y1] == 0 and (x1, y1, k) not in visited:
                            visited.add((x1, y1, k))
                            queue.append((x1, y1, k))
                        elif grid[x1][y1] == 1 and k - 1 >= 0 and (x1, y1, k - 1) not in visited:
                            visited.add((x1, y1, k - 1))
                            queue.append((x1, y1, k - 1))
            steps += 1
        return -1
                        
