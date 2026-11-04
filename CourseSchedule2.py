#210. Course Schedule II, Time - O(V+E)
class Solution:
    def findOrder(self, numCourses: int, prerequisites: list[list[int]]) -> list[int]:
        indegree = [0] * numCourses
        outdegree = defaultdict(list)
        result = []
        
        for course, pre in prerequisites:
            outdegree[pre].append(course)
            indegree[course] += 1  # Increment count
            
        queue = deque()
        courses = 0
        
        for i in range(numCourses):
            if indegree[i] == 0:
                queue.append(i)
                result.append(i)
                courses += 1
                
        while queue:
            temp = queue.popleft() # Use popleft for true BFS queue behavior
            for node in outdegree[temp]:
                indegree[node] -= 1  # O(1) decrement instead of .remove()
                if indegree[node] == 0:
                    courses += 1
                    queue.append(node)
                    result.append(node)
        
        if courses == numCourses:
            return result
        else:
            return []
