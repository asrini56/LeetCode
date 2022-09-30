#417. Pacific Atlantic Water Flow, Time/Space - O(m*n)
class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        result = []
        directions = [[-1,0],[1,0],[0,-1],[0,1]]
        def dfs(x,y,visited):
            visited[x][y] = True
            for direction in directions:
                i = x + direction[0]
                j = y + direction[1]
                if i < 0 or j < 0 or i >= len(heights) or j >= len(heights[i]) or visited[i][j] or heights[i][j] < heights[x][y]:
                    continue
                dfs(i,j,visited)
        pacific = [[False for i in range(len(heights[0]))] for j in range(len(heights))]
        atlantic = [[False for i in range(len(heights[0]))] for j in range(len(heights))]
        for i in range(len(heights)):
            dfs(i,0,pacific)
            dfs(i,len(heights[0])-1,atlantic)
        for j in range(len(heights[0])):
            dfs(0,j,pacific)
            dfs(len(heights)-1,j,atlantic)
        for i in range(len(heights)):
            for j in range(len(heights[i])):
                if pacific[i][j] and atlantic[i][j]:
                    result.append([i,j])
        return result
