#122. Best Time to Buy and Sell Stock II, Time - O(n)
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        dif = []
        n = len(prices)
        for i in range(0,n-1):
            dif.append(prices[i+1] - prices[i])
        dp = [0] * (n+1)
        dp1 = [0] * (n+1)
        for i in range(n-1):
            dp[i] = dif[i] + max(dp[i-1],dp1[i-2])
            dp1[i] = max(dp[i],dp1[i-1])
        return dp1[-3]
