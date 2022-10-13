class Solution: 
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        n = len(cost)
        dp, dp1, dp2 = 0, 0, 0  # corresponding to current dp, previous 1 step dp, previous 2 step dp 
        for i in range(2, n + 1):
            jumpOneStep = dp1 + cost[i-1]  # Minimum cost if we jump 1 step from floor (i-1)_th to i_th floor
            jumpTwoStep = dp2 + cost[i-2]  # Minimum cost if we jump 2 steps from floor (i-2)_th to i_th floor
            dp = min(jumpOneStep, jumpTwoStep)
            dp1, dp2 = dp, dp1
        return dp1
