class Solution:
    def canPartition(self, nums: list[int]) -> bool:
        if not nums:
            return False
        
        if sum(nums) % 2 !=0:
            return False
        total = sum(nums)//2

        dp = set()
        dp.add(0)

        for i in range(len(nums)-1,-1,-1):
            newDp = set()
            for value in dp:
                if nums[i] + value == total:
                    return True
                newDp.add(nums[i]+value)
                newDp.add(value)
            dp = newDp
        
        return False
