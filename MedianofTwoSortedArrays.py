#4. Median of Two Sorted Arrays, Time - O(log(min(m,n)))
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        if len(nums1) > len(nums2):
            return self.findMedianSortedArrays(nums2,nums1)
        x = len(nums1)
        y = len(nums2)
        low = 0
        high = x
        while low <= high:
            partitionX = (low+high)//2
            partitionY = (x+y+1)//2 - partitionX
            if partitionX == 0:
                minX = float("-inf")
            else:
                minX = nums1[partitionX-1]
            if partitionX == x:
                maxX = float("inf")
            else:
                maxX = nums1[partitionX]
            
            if partitionY == 0:
                minY = float("-inf")
            else:
                minY = nums2[partitionY-1]
            if partitionY == y:
                maxY = float("inf")
            else:
                maxY = nums2[partitionY]
            
            if minX <= maxY and minY <= maxX:
                if (x+y) % 2 == 0:
                    return (max(minX,minY)+min(maxX,maxY))/2
                else:
                    return max(minX,minY)
            elif minX > maxY:
                high = partitionX - 1
            else:
                low = partitionX + 1
            
