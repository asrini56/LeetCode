#16. 3Sum Closest, Time - O(n^2)
class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        diff = float('inf')
        nums.sort()
        for i in range(len(nums)-2):
            l = i+1
            h = len(nums)-1
            while l < h:
                t = nums[i] + nums[l] + nums[h]
                if abs(target - t) < abs(diff):
                    diff = (target - t)
                if t < target:
                    l = l + 1
                else:
                    h = h - 1
            if diff == 0:
                break
        return target - diff
