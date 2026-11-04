#Time - O(N)
class Solution:
    def longestSubarray(self, nums: list[int], limit: int) -> int:
        if not nums:
            return 0
        count = 0
        maxqueue = collections.deque()
        minqueue = collections.deque()
        left = 0

        for i in range(len(nums)):
            while maxqueue and nums[maxqueue[-1]] < nums[i]:
                maxqueue.pop()
            maxqueue.append(i)

            while minqueue and nums[minqueue[-1]] > nums[i]:
                minqueue.pop()
            minqueue.append(i)

            while (nums[maxqueue[0]] - nums[minqueue[0]]) > limit:
                left+=1
                while maxqueue[0] < left:
                    maxqueue.popleft()
                
                while minqueue[0] < left:
                    minqueue.popleft()
                
            count = max(count, i-left+1)
        
        return count
