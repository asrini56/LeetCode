#787. Cheapest Flights Within K Stops, Time - O(E+NLogN)
class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, K: int) -> int:
        ways = collections.defaultdict(dict)
        for a,b,c in flights:
            ways[a][b] = c
        heap = [(0,src,K+1)]
        while heap:
            p,i,k = heapq.heappop(heap)
            if i == dst:
                return p
            if k > 0:
                for j in ways[i]:
                    heapq.heappush(heap,(p+ways[i][j],j,k-1))
        return -1
