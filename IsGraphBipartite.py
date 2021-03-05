#785. Is Graph Bipartite?, Time - O(N+E)
class Solution:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        color = {}
        for node in range(len(graph)):
            if node not in color:
                stack = [node]
                color[node] = 0
                while stack:
                    node1 = stack.pop()
                    for n in graph[node1]:
                        if n not in color:
                            stack.append(n)
                            color[n] = color[node1]^1
                        elif color[n] == color[node1]:
                            return False
        return True
                
