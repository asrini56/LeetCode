#45. Jump Game II, Time - O(n)
class Solution:
    def jump(self, nums: List[int]) -> int:
        if len(nums) < 2:
            return 0
        l = r = 0
        steps = 0
        while r < len(nums) - 1:
            farthest = 0
            for i in range(l,r+1):
                farthest = max(farthest,i+nums[i])
            l = r +1
            r = farthest
            steps+=1
        return steps
