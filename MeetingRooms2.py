#253. Meeting Rooms II, Time - O(nlogn)
class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        free_rooms = []
        intervals.sort(key= lambda x: x[0])
        heapq.heappush(free_rooms,intervals[0][1])
        for i in range(1,len(intervals)):
            if free_rooms[0] <= intervals[i][0]:
                heapq.heappop(free_rooms)
            heapq.heappush(free_rooms,intervals[i][1])
        return len(free_rooms)
