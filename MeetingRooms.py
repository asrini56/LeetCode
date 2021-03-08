#252. Meeting Rooms, Time = O(nlogn)
class Solution:
    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:
        if not intervals:
            return True
        free = []
        intervals.sort(key = lambda x:x[0])
        heapq.heappush(free,intervals[0][1])
        for i in range(1,len(intervals)):
            if free[0] <= intervals[i][0]:
                heapq.heappop(free)
            heapq.heappush(free,intervals[i][1])
        if len(free) == 1:
            return True
        else:
            return False
