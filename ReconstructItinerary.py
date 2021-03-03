#332. Reconstruct Itinerary, [Euler Path Finding]
class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        destination = defaultdict(list)
        for dept, dest in sorted(tickets, reverse=True):
            destination[dept].append(dest)

        route = []
        stack = ['JFK']
        while stack:
            while destination[stack[-1]]:
                d = destination[stack[-1]].pop()
                stack.append(d)
            route.append(stack.pop())
        return list(reversed(route))
