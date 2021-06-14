#Time - O(n^3), Floyds Algorithm
class Solution:
    def findTheCity(self, n: int, edges: List[List[int]], maxd: int) -> int:
        dis = [[float('inf')] * n for _ in range(n)]
        for i, j, w in edges:
            dis[i][j] = dis[j][i] = w
        for i in range(n):
            dis[i][i] = 0
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    dis[i][j] = min(dis[i][j], dis[i][k] + dis[k][j])
        return min(reversed(range(n)), key=lambda x: sum(d <= maxd for d in dis[x]))
