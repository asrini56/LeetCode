#123. Best Time to Buy and Sell Stock III
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        k = 2
        dp = [[0 for d in prices] for t in range(k+1)]
        for t in range(1,k+1):
            maximum = float("-inf")
            for d in range(1,len(prices)):
                maximum = max(maximum,dp[t-1][d-1] - prices[d-1])
                dp[t][d] = max(dp[t][d-1],prices[d] + maximum)
        return dp[-1][-1]
