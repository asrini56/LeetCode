class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        stack = []
        max_area = 0
        heights.append(0)
        for i in range(len(heights)):
            start = i
            while stack and heights[i] < stack[-1][1]:
                index, height = stack.pop()
                width = i-index
                max_area = max(max_area,width*height)
                start = index
            
            stack.append((start,heights[i]))
        
        return max_area
