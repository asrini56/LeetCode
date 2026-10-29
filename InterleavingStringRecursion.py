class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        if len(s1) + len(s2) != len(s3):
            return False
        cache = {}
        n = len(s1)
        m = len(s2)

        def findways(i,j,cache):
            if i > n or j > m:
                return False
            
            if i == n and j == m:
                return True
            
            if (i,j) in cache:
                return cache[(i,j)]
            
            choose_i , choose_j = False , False

            if i < n and s1[i] == s3[i+j]:
                choose_i = findways(i+1,j, cache)
            if j < m and s2[j] == s3[i+j]:
                choose_j = findways(i,j+1, cache)
            
            cache[(i,j)] = choose_i or choose_j

            return cache[(i,j)]
        
        return findways(0,0,cache)
