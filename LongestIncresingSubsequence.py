#300. Longest Increasing Subsequence, Time - O(nlogn)
class Solution:
    def binarySearch(self,st,end,nums,indices,num):
        if st > end:
            return st
        while st <= end:
            middle = (st+end) // 2
            if nums[indices[middle]] < num:
                st = middle + 1
            else:
                end = middle - 1
        return st
    def lengthOfLIS(self, nums: List[int]) -> int:
        if len(nums) < 2:
            return len(nums)
        indices = [1] * (len(nums)+1)
        sequences = [None] * (len(nums))
        length = 0
        for i,num in enumerate(nums):
            newLength = self.binarySearch(1,length,nums,indices,num)
            sequences[i] = indices[newLength-1]
            indices[newLength] = i
            length = max(length,newLength)
        return length
