#213. House Robber II, Time - O(n)
class Solution:
    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0
        if len(nums) < 2:
            return nums[0]
        list1 = nums[1:]
        list2 = nums[:len(nums)-1]
        result = max(self.robFunc(list1),self.robFunc(list2))
        return result
        
    def robFunc(self, nums: List[int]) -> int:
        if not nums:
            return 0
        if len(nums) < 2:
            return nums[0]
        
        dp = [0] * len(nums)
        dp[0] = nums[0]
        dp[1] = max(nums[1],nums[0])
        for i in range(2,len(nums)):
            dp[i] = max(dp[i-1],nums[i] + dp[i-2])
        return dp[-1]
