#332. Reconstruct Itinerary, [Euler Path Finding]
# time - O(Elog E), where E is the number of tickets (edges).
from collections import defaultdict

class Solution:
    def findItinerary(self, tickets: list[list[str]]) -> list[str]:
        """
        Example Walkthrough:
        tickets = [["MUC","LHR"], ["JFK","MUC"], ["SFO","SJC"], ["LHR","SFO"]]
        
        1. Reverse Sort & Build Adjacency List:
           adj = {
               "SFO": ["SJC"],
               "MUC": ["LHR"],
               "LHR": ["SFO"],
               "JFK": ["MUC"]
           }
        2. Stack Traversal (Hierholzer's Algorithm):
           - Goes deep along the continuous chain until it hits a dead end:
             "JFK" -> "MUC" -> "LHR" -> "SFO" -> "SJC" (Dead end at SJC)
           - Pops dead ends backward into `path`:
             path = ["SJC", "SFO", "LHR", "MUC", "JFK"]
        3. Reverse Path:
           - Flips it back to the correct order:
             returns ["JFK", "MUC", "LHR", "SFO", "SJC"]
        """
        adj = defaultdict(list)

        # Sort in reverse so .pop() grabs the lexicographically smallest destination first
        for source, destination in sorted(tickets, reverse=True):
            adj[source].append(destination)
        
        stack = ["JFK"]
        path = []
        
        while stack:
            # While the current city still has unvisited outgoing flights
            while adj[stack[-1]]:
                city = adj[stack[-1]].pop()
                stack.append(city)
            
            # Hit a dead end: pop from stack and record in path
            path.append(stack.pop())
        
        # Reverse because dead ends were recorded first
        return list(reversed(path))
