#Trapping Rain Water
class Solution:
    def trap(self, height: List[int]) -> int:
        if not height:
            return 0
        rightMax = [0] * len(height)
        leftMax = [0] * len(height)
        leftMax[0] = height[0]
        l = height[0]
        r = height[len(height)-1]
        ans = 0
        rightMax[len(height)-1] = height[len(height)-1]
        for i in range(1,len(height)):
            if l < height[i]:
                l = height[i]
            leftMax[i] = l

        for i in range(len(height)-2,-1,-1):
            if r < height[i]:
                r = height[i]
            rightMax[i] = r
        
        
        for i in range(0,len(height)):
            minHeight = min(leftMax[i],rightMax[i])
            if height[i] < minHeight:
                ans += (minHeight - height[i])
        return ans
        
