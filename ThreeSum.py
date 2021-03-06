#15. 3Sum
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        if len(nums) < 3:
            return []
        nums.sort()
        n = len(nums)
        ans = []
        for i in range(0,n-2):
            left = i+1
            right = n-1
            while left < right:
                target = nums[i]+nums[left]+nums[right]
                if target == 0:
                    ans.append((nums[i],nums[left],nums[right]))
                    left = left +1
                    right = right - 1
                elif target < 0:
                    left = left + 1
                elif target > 0:
                    right = right - 1
        return set(ans)
