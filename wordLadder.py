class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList or not endWord or not beginWord or not wordList:
            return 0
        L = len(beginWord)
        
        com = defaultdict(list)
        for word in wordList:
            for i in range(L):
                com[word[:i]+'*'+word[i+1:]].append(word)
        
        queue = deque([(beginWord,1)])
        visited = set()
        visited.add(beginWord)
        while queue:
            curr,level = queue.popleft()
            for i in range(L):
                inter = curr[:i] + '*' + curr[i+1:]
                for word in com[inter]:
                    if word == endWord:
                        return level+1
                    if word not in visited:
                        visited.add(word)
                        queue.append((word,level+1))
                com[inter] = []
        return 0
