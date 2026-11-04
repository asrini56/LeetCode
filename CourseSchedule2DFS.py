class Solution:
    def findOrder(self, numCourses: int, prerequisites: list[list[int]]) -> list[int]:
        visited = defaultdict(int)
        result = []
        outdegree = collections.defaultdict(list)
        for course, pre in prerequisites:
            outdegree[course].append(pre)

        visited = [0] * numCourses

        def dfs(course):

            if visited[course] == 1:
                return False 
            elif visited[course] == 2:
                return True
            
            visited[course] = 1

            for dep in outdegree[course]:
                if not dfs(dep):
                    return False
            
            visited[course] = 2
            result.append(course)
            return True
        
        for i in range(numCourses):
            if visited[i] == 0:
                if not dfs(i):
                    return []

        return result
