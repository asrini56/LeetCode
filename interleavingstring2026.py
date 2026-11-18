class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        """
        ========================================================================
        STEP-BY-STEP WALKTHROUGH & EXAMPLE TRACE
        ========================================================================
        Example: s1 = "aab", s2 = "axy", s3 = "aaxby"

        1. LENGTH CHECK:
           - len(s1) = 3, len(s2) = 3, len(s3) = 6.
           - Since m + n (3 + 3 = 6) != len(s3) (6), it passes the length check.

        2. DP TABLE SETUP:
           - dp is a 2D boolean array of size (m+1) x (n+1) -> 4 x 4.
           - dp[i][j] represents whether the suffix s1[i:] and s2[j:] can form 
             the suffix s3[i+j:].
           - Base Case: dp[3][3] = True (empty suffixes match empty s3 suffix).

        3. BACKWARD ITERATION (Right to Left, Bottom to Top):
           - We fill the table from i = 3 down to 0 and j = 3 down to 0.
           - At each cell (i, j), we check two choices:
             a) Can we take a character from s1? (s1[i] == s3[i+j] and dp[i+1][j])
             b) Can we take a character from s2? (s2[j] == s3[i+j] and dp[i][j+1])

        4. FINAL RESULT:
           - Returns dp[0][0], which evaluates to True if s1 and s2 can 
             completely interleave to form s3.
        ========================================================================
        """
        m, n = len(s1), len(s2)
        if m + n != len(s3):
            return False
        
        dp = [[False for i in range(n+1)] for j in range(m+1)]

        dp[m][n] = True

        for i in range(m,-1,-1):
            for j in range(n,-1,-1):
                if i < m and s1[i] == s3[i+j] and dp[i+1][j]:
                    dp[i][j] = True
                if j < n and s2[j] == s3[i+j] and dp[i][j+1]:
                    dp[i][j] = True
        
        return dp[0][0]
