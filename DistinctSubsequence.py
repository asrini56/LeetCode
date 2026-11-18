class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        """
        ========================================================================
        STEP-BY-STEP WALKTHROUGH & CONCRETE EXAMPLE TRACE
        ========================================================================
        Problem: Distinct Subsequences (LeetCode 115)
        Example: s = "rabbbit", t = "rabbit"

        1. BASE CHECKS:
           - len(s) = 7, len(t) = 6. Valid.

        2. RECURSIVE DFS WITH MEMOIZATION (dfs(i, j, memo)):
           - i points to s, j points to t.
           - At each step, we explore two branches:
             a) Skip: dfs(i + 1, j) -> always try skipping s[i].
             b) Match: if s[i] == t[j], add dfs(i + 1, j + 1).

        3. TRACE WALKTHROUGH (Bottom-Up View / Subproblems):
           - i=0 ('r'), j=0 ('r'): Matches! Branches into (skip: dfs(1,0)) + (match: dfs(1,1)).
             - In "rabbbit", the three 'b's at indices 2, 3, 4 match the single 'b' at index 2 in "rabbit".
             - The algorithm branches and accumulates valid paths where each 'b' is chosen.
           - Memoization caches results for `(i, j)` to avoid re-evaluating overlapping subproblems.

        4. FINAL RESULT:
           - Returns dfs(0, 0, {}), which evaluates to 3.
        ========================================================================
        """
        if not s or not t:
            return 0
        
        if len(t) > len(s):
            return 0
        
        n = len(s)
        
        def dfs(i, j, memo):
            # Base Case 1: Successfully matched entire target string t
            if j == len(t):
                return 1
            
            # Base Case 2: Ran out of characters in s before finishing t
            if i >= len(s):
                return 0
            
            # Return memoized result if already computed
            if (i, j) in memo:
                return memo[(i, j)]
            
            # Choice 1: Skip current character in s
            ways = dfs(i + 1, j, memo)

            # Choice 2: Match current character if s[i] == t[j]
            if s[i] == t[j]:
                ways += dfs(i + 1, j + 1, memo)
            
            # Save to memo table and return
            memo[(i, j)] = ways
            return memo[(i, j)]
        
        return dfs(0, 0, {})
