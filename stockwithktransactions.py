class Solution:
    def maxProfit(self, k: int, prices: list[int]) -> int:
        """
        ========================================================================
        STEP-BY-STEP WALKTHROUGH & INTUITION (Best Time to Buy and Sell Stock IV)
        ========================================================================
        Problem: LeetCode 188 - At most k transactions
        Time Complexity: O(k * n)
        Space Complexity: O(n) using rolling arrays

        1. ROLLING ARRAYS (Space Optimization):
           - Instead of a 2D table of size (k+1) x n, we only need the previous 
             transaction's results to compute the current one.
           - `oddProfit`: Tracks max profits for odd transaction counts (1, 3, 5...).
           - `evenProfit`: Tracks max profits for even transaction counts (0, 2, 4...).

        2. THE `maxThusFar` INTUITION:
           - On each day `d`, `maxThusFar` dynamically tracks the best "net worth" 
             after buying a stock on some previous day `j` (where `j < d`), factoring 
             in accumulated profits from the previous transaction up to day `j-1`:
               `maxThusFar = max(maxThusFar, previousProfit[d-1] - prices[d-1])`
           - This assumes we either keep our previous optimal buy point or decide 
             to make a brand new purchase using yesterday's profit baseline. This 
             drops the inner loop from O(n^2) to O(n).

        3. DECISION LOGIC (`currentProfit[d]`):
           - For each day, we take the maximum of two choices:
             a) Do nothing today: Carry over `currentProfit[d-1]`.
             b) Sell today: Combine today's stock price (`prices[d]`) with our 
                best historical buy point (`maxThusFar`).
               `currentProfit[d] = max(currentProfit[d-1], prices[d] + maxThusFar)`

        4. FINAL RESULT:
           - Returns `evenProfit[-1]` if k is even, or `oddProfit[-1]` if k is odd.

        ========================================================================
        CONCRETE EXAMPLE WALKTHROUGH
        ========================================================================
        Input: k = 2, prices = [3, 2, 6, 5, 0, 3]

        INITIALIZATION:
        - oddProfit  = [0, 0, 0, 0, 0, 0]
        - evenProfit = [0, 0, 0, 0, 0, 0]

        --- TRANSACTION 1 (i = 1, current = oddProfit, previous = evenProfit) ---
        - d = 1 (price=2): maxThusFar = max(-inf, 0 - 3) = -3
          oddProfit[1] = max(0, 2 + (-3)) = 0
        - d = 2 (price=6): maxThusFar = max(-3, 0 - 2) = -2
          oddProfit[2] = max(0, 6 + (-2)) = 4  (Buy at 2, sell at 6)
        - d = 3 (price=5): maxThusFar = max(-2, 0 - 6) = -2
          oddProfit[3] = max(4, 5 + (-2)) = 4
        - d = 4 (price=0): maxThusFar = max(-2, 0 - 5) = -2
          oddProfit[4] = max(4, 0 + (-2)) = 4
        - d = 5 (price=3): maxThusFar = max(-2, 0 - 0) = 0
          oddProfit[5] = max(4, 3 + 0) = 4
        - Result after T1: oddProfit = [0, 0, 4, 4, 4, 4]

        --- TRANSACTION 2 (i = 2, current = evenProfit, previous = oddProfit) ---
        - d = 1 (price=2): maxThusFar = max(-inf, oddProfit[0] - 3) = -3
          evenProfit[1] = max(0, 2 + (-3)) = 0
        - d = 2 (price=6): maxThusFar = max(-3, oddProfit[1] - 2) = -2
          evenProfit[2] = max(0, 6 + (-2)) = 3
        - d = 3 (price=5): maxThusFar = max(-2, oddProfit[2] - 6) = max(-2, 4 - 6) = -2
          evenProfit[3] = max(3, 5 + (-2)) = 3
        - d = 4 (price=0): maxThusFar = max(-2, oddProfit[3] - 5) = max(-2, 4 - 5) = -1
          evenProfit[4] = max(3, 0 + (-1)) = 3
        - d = 5 (price=3): maxThusFar = max(-1, oddProfit[4] - 0) = max(-1, 4 - 0) = 4
          evenProfit[5] = max(3, 3 + 4) = 7  (T1: buy 2 sell 6 [4] + T2: buy 0 sell 3 [3] = 7)
        - Result after T2: evenProfit = [0, 0, 3, 3, 3, 7]

        FINAL RETURN:
        - Since k = 2 (even), returns evenProfit[-1] -> 7.
        ========================================================================
        """
        if not prices:
            return 0
        
        oddProfit = [0] * len(prices)
        evenProfit = [0] * len(prices)

        for i in range(1, k + 1):
            maxThusFar = float("-inf")
            
            # Alternate between odd and even transaction profit arrays
            if i % 2 == 0:
                currentProfit = evenProfit
                previousProfit = oddProfit
            else:
                currentProfit = oddProfit
                previousProfit = evenProfit
            
            for d in range(1, len(prices)):
                # Track best (previous profit minus buy price) up to yesterday
                maxThusFar = max(maxThusFar, previousProfit[d - 1] - prices[d - 1])
                
                # Max of skipping today (carrying over) or selling today
                currentProfit[d] = max(currentProfit[d - 1], prices[d] + maxThusFar)
        
        # Return final profit at the last day depending on whether k is even or odd
        return evenProfit[-1] if k % 2 == 0 else oddProfit[-1]
