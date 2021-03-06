#322. Coin Change, Time - O(S∗n)
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [float("inf")] * (amount + 1)
        dp[0] = 0
        for coin in coins:
            for amt in range(coin,amount+1):
                dp[amt] = min(dp[amt],dp[amt-coin]+1)
        if dp[amount] != float("inf"):
            return dp[amount]
        else:
            return -1
