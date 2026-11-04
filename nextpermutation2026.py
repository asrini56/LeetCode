class Solution:
    def nextPermutation(self, nums: list[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        def reverse(nums,st,end):
            while st < end:
                nums[st],nums[end] = nums[end],nums[st]
                st+=1
                end-=1
        
        n = len(nums)
        i = n-1

        while i>=1 and nums[i] <= nums[i-1]:
            i-=1
        if i != 0:
            j = i

            while j+1 < n and nums[j+1] > nums[i-1]:
                j+=1
        
            nums[j],nums[i-1] = nums[i-1],nums[j]
        
        reverse(nums,i,n-1)
"""
Example 1:

Input: nums = [1,2,3]
Output: [1,3,2]
Example 2:

Input: nums = [3,2,1]
Output: [1,2,3]
Example 3:

Input: nums = [1,1,5]
Output: [1,5,1]

"""
