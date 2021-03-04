#78. Subsets, Time - O(N*2^N)
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        ans = []
        def subset(st = 0,curr = []):
            if len(curr) == k:
                ans.append(curr[:])
                return
            for i in range(st,len(nums)):
                curr.append(nums[i])
                subset(i+1,curr)
                curr.pop()
        for k in range(len(nums)+1):
            subset()
        return ans
