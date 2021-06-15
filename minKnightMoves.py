#DFS - TIME - O(X*Y)
class Solution:
    def minKnightMoves(self, x: int, y: int) -> int:
        @lru_cache(None) 
        def dp(x,y):
            if x + y == 0: return 0
            elif x + y == 2: return 2
            return min(dp(abs(x-1),abs(y-2)), dp(abs(x-2),abs(y-1))) + 1
        return dp(abs(x),abs(y))

#BFS - 
class Solution:
    def minKnightMoves(self, x: int, y: int) -> int:
        q = collections.deque([(0, 0, 0)])
        x, y, visited = abs(x), abs(y), set([(0,0)])
        while q:
            a, b, step = q.popleft()
            if (a, b) == (x,y): return step
            for dx, dy in [(1,2),(2,1),(1,-2),(2,-1),(-1,2),(-2,1)]:  # no need to have (-1, -2) and (-2, -1) since it only goes 1 direction
                if (a+dx, b+dy) not in visited and -1 <= a+dx <= x+2 and -1 <= b+dy <= y+2:
                    visited.add((a+dx, b+dy))
                    q.append((a+dx, b+dy, step+1))
        return -1
#MATHS - O(1)
class Solution:
    def minKnightMoves(self, x: int, y: int) -> int:
        x, y = abs(x), abs(y)
        if (x < y): x, y = y, x
        if (x == 1 and y == 0): return 3        
        if (x == 2 and y == 2): return 4        
        delta = x - y
        if (y > delta): return delta - 2 * int((delta - y) // 3);
        else: return delta - 2 * int((delta - y) // 4);
