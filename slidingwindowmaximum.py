#239. Sliding Window Maximum, Time - O(n)
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        ans = []
        queue = collections.deque()
        for i, v in enumerate(nums):
            if queue and queue[0] <= i-k:
                queue.popleft()
            while queue and nums[queue[-1]] < nums[i]:
                queue.pop()
            queue.append(i)
            if i+1 >= k:
                ans.append(nums[queue[0]])
        return ans
