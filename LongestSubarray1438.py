#1438. Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit, Time - O(n)
class Solution:
    def longestSubarray(self, nums: List[int], limit: int) -> int:
        left = 0
        right = 0
        result = 1
        minDeque = deque([0])
        maxDeque = deque([0])
        for right in range(1,len(nums)):
            while minDeque and nums[minDeque[-1]] > nums[right]:
                minDeque.pop()
            minDeque.append(right)
            
            while maxDeque and nums[maxDeque[-1]] < nums[right]:
                maxDeque.pop()
            maxDeque.append(right)
            
            while nums[maxDeque[0]] - nums[minDeque[0]] > limit:
                left+=1
                if maxDeque[0] < left:
                    maxDeque.popleft()
                if minDeque[0] < left:
                    minDeque.popleft()
            
            result = max(result,right-left+1)
        
        return result
