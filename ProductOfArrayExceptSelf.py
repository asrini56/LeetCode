#238. Product of Array Except Self, Time - O(n)
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        left = [1] * len(nums)
        right = [1] * len(nums)
        ans = []
        for i in range(1,len(nums)):
            left[i] = nums[i-1] * left[i-1]
        for j in range(len(nums)-2,-1,-1):
            right[j] = right[j+1] * nums[j+1]
        
        for i in range(len(nums)):
            ans.append(left[i] * right[i])
        
        return ans
        
