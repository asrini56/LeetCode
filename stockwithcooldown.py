from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        """
        Solves LeetCode 309: Best Time to Buy and Sell Stock with Cooldown.
        
        The challenge is the cooldown rule: after selling, you cannot buy on the next day.
        This approach models the problem as a Finite State Machine (FSM) with three states:
        
        1. hold: You currently own a stock.
           - How you get here: Either you were already holding it from a previous day (prev_hold), 
             OR you were in a cooldown/reset state and just bought a stock today (prev_reset - prices[i]).
             
        2. sold: You just sold the stock you were holding.
           - How you get here: You must have been holding a stock yesterday and sold it today 
             (prev_hold + prices[i]). Because of the cooldown rule, you are forced into this state temporarily.
             
        3. reset (Cooldown/Neutral): You do not own a stock, and you are allowed to buy one.
           - How you get here: Either you stayed in reset yesterday (prev_reset), 
             OR you just finished your mandatory cooldown day after selling yesterday (prev_sold).
        """
        if not prices:
            return 0
        
        # State variables representing the max profit up to the current day
        hold = -prices[0]       # Currently holding a stock (bought on day 0)
        sold = float('-inf')    # Just sold a stock (impossible on day 0)
        reset = 0               # Cooldown / neutral state (doing nothing)
        
        for i in range(1, len(prices)):
            # Cache previous states before updating
            prev_hold = hold
            prev_sold = sold
            prev_reset = reset

            # State transition equations
            hold = max(prev_hold, prev_reset - prices[i])
            sold = prev_hold + prices[i]
            reset = max(prev_reset, prev_sold)
            
        # We can end our sequence either in the 'sold' state or 'reset' state
        return max(sold, reset)

# --- Example Usage ---
sol = Solution()
prices = [1, 2, 3, 0, 2]
result = sol.maxProfit(prices)
print(f"Max profit for {prices}: {result}")  
# Output: 3
# Explanation: buy at 1, sell at 2 (profit = 1), cooldown, buy at 0, sell at 2 (profit = 2) -> Total = 3
