#72. Edit Distance, Time/Space - O(n*m)
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        """
        ========================================================================
        STEP-BY-STEP WALKTHROUGH & TABLE VISUALIZATION (Edit Distance / Levenshtein)
        ========================================================================
        Example: word1 = "horse", word2 = "ros"

        1. DP TABLE DIMENSIONS & SETUP:
           - dp is a 2D table of size (m+1) x (n+1) -> (5+1) x (3+1) = 6 x 4.
           - Rows represent prefixes of word1 (plus an empty prefix at index 0).
           - Columns represent prefixes of word2 (plus an empty prefix at index 0).
           - Base Cases: 
             - dp[i][0] = i (converting word1[:i] to an empty string requires i deletions).
             - dp[0][j] = j (converting an empty string to word2[:j] requires j insertions).

        2. DP TABLE POPULATION (for word1 = "horse", word2 = "ros"):
           - Indices:
             Columns -> "" (j=0), 'r' (j=1), 'o' (j=2), 's' (j=3)
             Rows:
               "" (i=0): [0, 1, 2, 3]
              'h' (i=1): [1, 1, 2, 3]
              'o' (i=2): [2, 2, 1, 2]
              'r' (i=3): [3, 2, 2, 2]
              's' (i=4): [4, 3, 3, 2]
              'e' (i=5): [5, 4, 4, 3]

        3. STATE TRANSITION LOGIC:
           - If characters match (word1[i-1] == word2[j-1]):
             dp[i][j] = dp[i-1][j-1] (carry over cost from diagonal)
           - If characters differ:
             dp[i][j] = 1 + min(
                 dp[i-1][j-1],  # Substitution
                 dp[i-1][j],    # Deletion
                 dp[i][j-1]     # Insertion
             )

        4. FINAL RESULT:
           - Returns dp[-1][-1] (bottom-right cell), which is 3.
        ========================================================================
        """
        if not word1 and word2:
            return len(word2)
        elif not word2 and word1:
            return len(word1)
        elif not word1 and not word2:
            return 0
        m = len(word1)
        n = len(word2)
        dp = [[0 for i in range(n+1)] for j in range(m+1)]

        for i in range(0, m+1):
            dp[i][0] = i
        
        for j in range(0, n+1):
            dp[0][j] = j
        
        for i in range(1, m+1):
            for j in range(1, n+1):
                if word1[i-1] == word2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1])
        
        return dp[-1][-1]
