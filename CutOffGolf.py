#675. Cut Off Trees for Golf Event,Time - O((RC)^2) 
import collections
class Solution:
    def cutOffTree(self, forest: List[List[int]]) -> int:
        m, n = len(forest), len(forest[0])
        trees = []
        for i in range(len(forest)):
            for j in range(len(forest[i])):
                v = forest[i][j]
                if v > 1:
                    trees.append((v,i,j))
        trees.sort()
        sr, sc = 0, 0
        total = 0
        for tree in trees:
            value,tr,tc = tree
            distance = self.bfs(forest,sr, sc, tr, tc, m, n)
            if distance < 0:
                return -1
            total+=distance
            sr,sc=tr,tc
        return total
    def bfs(self,forest,sr, sc, tr, tc, m, n):
        queue = collections.deque([(sr, sc, 0)])
        visited = set()
        visited.add((sr,sc))
        while queue:
            r, c, d = queue.popleft()
            if r == tr and c == tc:
                return d
            for nr,nc in ((r-1, c), (r+1, c), (r, c-1), (r, c+1)):
                if (0 <= nr < m and 0 <= nc < n and (nr, nc) not in visited and forest[nr][nc]):
                    visited.add((nr,nc))
                    queue.append((nr,nc,d+1))
        return -1
                    
                    
