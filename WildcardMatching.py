#44. Wildcard Matching
class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        m = len(p)
        n = len(s)
        T = [[None] * (n + 1) for _ in range(m + 1)]

        # Recursion Base Cases
        # (1) p: "" matches s: ""
        T[0][0] = True 

        # (2) p: "" does not match non-empty s
        for j in range(1, n + 1):
            T[0][j] = False

        # (3) For T[i][0] = True, p must be '*', '**', '***', etc. 
        #     Once p[i-1] != '*', all the T[i][0] afterwards will be False
        for i in range(1, m + 1):
            if p[i-1] == '*':
                T[i][0] = T[i-1][0]
            else:
                T[i][0] = False

        # Fill the table T (using recursion formulation -> see recursion code)      
        for i in range(1, m + 1):
            for j in range(1, n + 1):

                pIdx = i - 1  # Because p length in m and last index is m - 1
                sIdx = j - 1  # Because s length is n and last index is n - 1

                # (i-1)th char matches (j-1)th char or (i-1)th char matches single char
                if p[pIdx] == s[sIdx] or p[pIdx] == '?': 
                    T[i][j] = T[i-1][j-1]

                # (i-1)th char matches any sequence of chars
                elif p[pIdx] == '*':

                    # Recurrence relation in 2 variables: F(n,m) = F(n-1,m) + F(n,m-1)
                    T[i][j] = T[i-1][j] or T[i][j-1]

                else:
                    T[i][j] = False

        return T[m][n]
