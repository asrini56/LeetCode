#787. Cheapest Flights Within K Stops, Time - O(E+NLogN)
"""
put all flights into a prices map -> Map<Integer, Map<Integer, Integer>>
// source city : Map<destination city, price>
init a min pq -> each object in pq should be an int array with
top[0] = current total price
top[1] = current source city
top[2] = max distance to destination allowed
pq compares each object by total price so far
add original source city to pq with price = 0 & distance allowed = k + 1
while exists cities to explore
--> get min object then remove it from pq
--> get current total price, current source city & distance to destination allowed from min object
--> if current source == destination (obviously distance from original source to current source [which is destination] is less than k) -> return current total price
else find (from prices map) all connected flights that fly from current source + calculate new price, new current source & new distance + add them to pq
If no city left to explore and no flight that fits criteria found till now, return -1
"""
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
