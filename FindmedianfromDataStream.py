#Find Median from Data Stream, Time - O(logn)
class MedianFinder:

    def __init__(self):
        """
        initialize your data structure here.
        """
        
        self.left = []
        self.right = []
        

    def addNum(self, num: int) -> None:
        if not self.left or num <= -self.left[0]:
            heapq.heappush(self.left, -num) # we use negative numbers to make it a max heap, default python heap is a min heap
        else:
            heapq.heappush(self.right, num)
            
        # rebalance here
        if abs(len(self.left) - len(self.right)) > 1:
            if len(self.left) > len(self.right):
                elt = -heapq.heappop(self.left) # negate to get it back to original number
                heapq.heappush(self.right, elt)
            else:
                elt = heapq.heappop(self.right)
                heapq.heappush(self.left, -elt) # negate due to max heap


    def findMedian(self) -> float:
        
        # remember to negate the left values!
        
        if len(self.left) == len(self.right):
            return (-self.left[0] + self.right[0]) / 2
        elif len(self.left) > len(self.right):
            return -self.left[0]
        else:
            return self.right[0]


# Your MedianFinder object will be instantiated and called as such:
# obj = MedianFinder()
# obj.addNum(num)
# param_2 = obj.findMedian()
