#189. Rotate Array, Time - O(n), Space - O(1)
class Solution:
    def reverse(self, nums: list, start: int, end: int) -> None:
        while start < end:
            nums[start], nums[end] = nums[end], nums[start]
            start, end = start + 1, end - 1
                
    def rotate(self, nums: List[int], k: int) -> None:
        n = len(nums)
        k %= n
        #reverse list
        self.reverse(nums, 0, n - 1)
        #reverse till k-1 elements in list
        self.reverse(nums, 0, k - 1)
        #reverse elements from k to end
        self.reverse(nums, k, n - 1)
