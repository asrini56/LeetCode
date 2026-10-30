class Solution:
    def missingNumber(self, nums: list[int]) -> int:
        res = len(nums)

        for i in range(len(nums)):
            res = res ^ (i^nums[i])
        
        return res
