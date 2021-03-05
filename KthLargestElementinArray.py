#215. Kth Largest Element in an Array
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        def swap(left,right,nums):
            nums[left],nums[right] = nums[right],nums[left]
        def quickSelect(nums,st,end,pos):
            while True:
                if st > end:
                    break
                else:
                    pivot = st
                    left = st + 1
                    right = end
                    while left <= right:
                        if nums[left] > nums[pivot] and nums[right] < nums[pivot]:
                            swap(left,right,nums)
                        if nums[left] <= nums[pivot]:
                            left+=1
                        if nums[right] >= nums[pivot]:
                            right -= 1
                    swap(pivot,right,nums)
                    if right == pos:
                        return nums[right]
                    if right < pos:
                        st = right + 1
                    else:
                        end = right - 1
        pos = len(nums) - k
        return quickSelect(nums,0,len(nums)-1,pos)
        
