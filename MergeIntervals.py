#56. Merge Intervals, Time - O(n)
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if len(intervals) < 2:
            return intervals
        intervals.sort()
        arr = []
        arr.append(intervals[0])
        
        for i in range(1,len(intervals)):
            if arr[-1][1] >= intervals[i][0]:
                arr[-1][1] = max(arr[-1][1],intervals[i][1])
            else:
                arr.append(intervals[i])
        return arr
