class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        """
        Example Walkthrough for heights = [2, 1, 5]
        
        1. Preprocessing:
           - Append 0 to heights -> [2, 1, 5, 0]
           - stack = [], max_area = 0
        
        2. Loop Execution:
           - i = 0, heights[0] = 2:
             - stack is empty. Append (0, 2).
             - stack = [(0, 2)], max_area = 0
           
           - i = 1, heights[1] = 1:
             - heights[1] (1) < stack[-1][1] (2) -> True. Pop (0, 2).
             - index = 0, height = 2, width = 1 - 0 = 1.
             - max_area = max(0, 1 * 2) = 2.
             - start = index -> 0.
             - Append (0, 1).
             - stack = [(0, 1)], max_area = 2
           
           - i = 2, heights[2] = 5:
             - heights[2] (5) < stack[-1][1] (1) -> False.
             - Append (2, 5).
             - stack = [(0, 1), (2, 5)], max_area = 2
           
           - i = 3, heights[3] = 0 (sentinel):
             - heights[3] (0) < stack[-1][1] (5) -> True. Pop (2, 5).
             - width = 3 - 2 = 1, area = 1 * 5 = 5. max_area = 5. start = 2.
             - Next: heights[3] (0) < stack[-1][1] (1) -> True. Pop (0, 1).
             - width = 3 - 0 = 3, area = 3 * 1 = 3. max_area = max(5, 3) = 5. start = 0.
             - Append (0, 0).
             - stack = [(0, 0)], max_area = 5
        
        3. Final Return:
           - Returns max_area = 5.
        """
        stack = []
        max_area = 0
        heights.append(0)
        for i in range(len(heights)):
            start = i
            while stack and heights[i] < stack[-1][1]:
                index, height = stack.pop()
                width = i - index
                max_area = max(max_area, width * height)
                # Extend the starting index of the current bar backwards to the popped bar's index.
                # This ensures that when a taller bar is popped, the current shorter bar (or future bars)
                # inherits its leftmost boundary, correctly accounting for its width contribution.
                start = index
            
            stack.append((start, heights[i]))
        
        return max_area
