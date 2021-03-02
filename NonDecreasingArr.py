#665. Non-decreasing Array, Time - O(n)
class Solution:
    def checkPossibility(self, nums: List[int]) -> bool:
        check = 0
        for i in range(len(nums)-1):
            if nums[i] > nums[i+1]:
                check+=1
            if check > 1 or ((i-1 >= 0 and nums[i-1] > nums[i+1]) and (i+2 <len(nums) and nums[i+2] < nums[i])):
                return False
        return True
