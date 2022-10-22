#797. All Paths From Source to Target, Time - n*(2^n)
class Solution:
    def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
        n = len(graph)-1
        result = []
        def dfs(formed):
            if formed[-1] == n:
                result.append(formed)
                return
            for child in graph[formed[-1]]:
                dfs(formed + [child])
        dfs([0])
        return result
