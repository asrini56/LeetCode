class Solution:
    def nextLargerElement(self,nums1,n):
        #code here
        mapping = {}
        stack = []
        stack.append([nums1[0],0])
        answer = []
        for i in range(1,len(nums1)):
            while stack and nums1[i] > stack[-1][0]:
                mapping[stack[-1][1]] = nums1[i]
                stack.pop()
            stack.append([nums1[i],i])
        for element in stack:
            mapping[element[1]] = -1
        mapping[len(nums1)-1] = -1
        for i in range(len(nums1)):
            answer.append(mapping[i])
        return answer
