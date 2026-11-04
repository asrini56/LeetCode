class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        """
        Solves LeetCode 97: Interleaving String using 2D Dynamic Programming.
        
        Example Walkthrough:
            s1 = "aabcc"
            s2 = "dbbca"
            s3 = "aadbbcbcac"
            
            DP Table Result (dp[0][0] = True):
                   d     b     b     c     a    ""
                -------------------------------------
            a | True  True  False False False False
            a | True  True  True  True  True  False
            b | False True  True  True  True  False
            c | False False False True  True  False
            c | False False False False True  True
           "" | False False False False False True
        """
        m, n = len(s1), len(s2)
        
        # Length check: combined lengths must equal s3 length
        if m + n != len(s3):
            return False
        
        # Initialize (m + 1) x (n + 1) DP table with False
        dp = [[False for _ in range(n + 1)] for _ in range(m + 1)]

        # Base case: empty suffixes match the end of s3
        dp[m][n] = True

        # Fill the table bottom-up from (m, n) down to (0, 0)
        for i in range(m, -1, -1):
            for j in range(n, -1, -1):
                if i == m and j == n:
                    continue
                
                # Option 1: Match character from s1
                if i < m and s1[i] == s3[i + j] and dp[i + 1][j]:
                    dp[i][j] = True
                
                # Option 2: Match character from s2
                if j < n and s2[j] == s3[i + j] and dp[i][j + 1]:
                    dp[i][j] = True
        
        return dp[0][0]

# --- Example Usage ---
sol = Solution()
s1 = "aabcc"
s2 = "dbbca"
s3 = "aadbbcbcac"

result = sol.isInterleave(s1, s2, s3)
print(f"Can '{s1}' and '{s2}' interleave to form '{s3}'? {result}")  
# Output: True
