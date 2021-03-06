#210. Course Schedule II, Time - O(V+E)
class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        visited = []
        courseDict=defaultdict(list)
        indegree = defaultdict(set)
        outdegree = defaultdict(set)
        for i,j in prerequisites:
            outdegree[j].add(i)
            indegree[i].add(j)
        cr = 0
        ans = []
        st = []
        #Checking and adding nodes with 0 indegree to ans,st
        for i in range(numCourses):
            if not indegree[i]:
                ans.append(i)
                st.append(i)
        while st:
            node = st.pop()
            #Checking and removing node from all connections
            for x in outdegree[node]:
                indegree[x].remove(node)
                if not indegree[x]:
                    ans.append(x)
                    st.append(x)
        if len(ans) == numCourses:
            return ans
        else:
            return []
