#Time - O(n)
class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        if newInterval:
            count = 0
            for i in range(len(intervals)):
                if intervals[i][0] >= newInterval[0]:
                    break
                count+=1
            intervals.insert(count,newInterval)
        result = [intervals[0]]
        for i in range(1,len(intervals)):
            if result[-1][1] >= intervals[i][0]:
                result[-1][1] = max(result[-1][1],intervals[i][1])
            else:
                result.append(intervals[i])
        return result
