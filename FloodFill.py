#733. Flood Fill, Time - O(N)
class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, newColor: int) -> List[List[int]]:
        check = image[sr][sc]
        R, C = len(image), len(image[0])
        if check == newColor:
            return image
        def dfs(image,sr,sc):
            if sr > len(image) or sc > len(image[0]) or not 0<=sr or not 0<=sc:
                return
            if image[sr][sc] == check:
                image[sr][sc] = newColor
                if sr >= 1: dfs(image,sr-1, sc)
                if sr+1 < R: dfs(image,sr+1, sc)
                if sc >= 1: dfs(image,sr, sc-1)
                if sc+1 < C: dfs(image,sr, sc+1)
        dfs(image,sr,sc)
        return image
