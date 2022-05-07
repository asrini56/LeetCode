#456 - 132 Pattern
#Time and Space - O(n)
class Solution:
    def find132pattern(self, nums: List[int]) -> bool:
        minimum = []
        minList = [nums[0]]
        stack = []
        for i in range(1,len(nums)):
            if nums[i] < minList[-1]:
                minList.append(nums[i])
            else:
                minList.append(minList[-1])
        for j in range(len(nums)-1,-1,-1):
            if nums[j] > minList[j]:
                while stack and stack[-1] <= minList[j]:
                    stack.pop()
                if stack and stack[-1] < nums[j]:
                    return True
                stack.append(nums[j])
        return False
