#496. Next Greater Element I, Time - O(N)
class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        mapping = {}
        stack = []
        stack.append(nums2[0])
        answer = []
        for i in range(1,len(nums2)):
            while stack and nums2[i] > stack[-1]:
                mapping[stack[-1]] = nums2[i]
                stack.pop()
            stack.append(nums2[i])
        
        for element in stack:
            mapping[element] = -1
        
        for i in range(len(nums1)):
            answer.append(mapping[nums1[i]])
        
        return answer
