class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        if not s or not t:
            return 0
        
        if len(t) > len(s):
            return 0
        
        n = len(s)
        
        def dfs(i,j, memo):

            if j == len(t):
                return 1
            
            if i >= len(s):
                return 0
            
            if (i,j) in memo:
                return memo[(i,j)]
            ways = dfs(i+1,j,memo)

            if s[i] == t[j]:
                ways+=dfs(i+1,j+1, memo)
            
            memo[(i,j)] = ways

            return memo[(i,j)]
        
        return dfs(0,0,{})
