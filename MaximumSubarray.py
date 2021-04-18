#53. Maximum Subarray, Time - O(n)
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        if not nums:
            return 0
        curr = ans = nums[0]
        for num in nums[1:]:
            curr = max(num,curr+num)
            ans = max(ans,curr)
        return ans
