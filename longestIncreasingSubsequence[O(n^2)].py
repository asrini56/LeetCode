#time - o(n^2)
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        length = [1] * len(nums)
        sequences = [None] * len(nums)
        for i in range(len(nums)):
            for j in range(0,i):
                if nums[j] < nums[i]:
                    length[i] = max(length[j]+1,length[i])
                    sequences[i] = j
        return max(length)
