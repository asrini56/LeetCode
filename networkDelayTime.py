#743. Network Delay Time, Time - O(N+ElogN), The maximum number of vertices that could be added to the priority queue is E
class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        network = defaultdict(list)
        total = [0] + [float("inf")] * n
        for u,v,w in times:
            network[u].append([v,w])
        ans = 0
        heap = [(0,k)]
        count = 0
        while heap:
            time,node = heapq.heappop(heap)
            if time < total[node]:
                total[node] = time
                for neighbour in network[node]:
                    heapq.heappush(heap,(time+neighbour[1],neighbour[0]))
        ans = max(total)
        if ans != float("inf"):
            return ans
        return -1
