#283. Move Zeroes
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        curr = 0
        l = 0
        n = len(nums)
        while curr < n:
            if nums[curr] == 0:
                nums.pop(curr)
                nums.append(0)
                n -= 1
            else:
                curr+=1
