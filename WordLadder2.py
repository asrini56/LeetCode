def findLadders(self, beginWord, endWord, wordList):
	"""
	:type beginWord: str
	:type endWord: str
	:type wordList: List[str]
	:rtype: List[List[str]]
	"""
	if not endWord or not beginWord or not wordList or endWord not in wordList \
		or beginWord == endWord:
		return []

	L = len(beginWord)

	# Dictionary to hold combination of words that can be formed,
	# from any given word. By changing one letter at a time.
	all_combo_dict = collections.defaultdict(list)
	for word in wordList:
		for i in range(L):
			all_combo_dict[word[:i] + "*" + word[i+1:]].append(word)

	# Build graph, BFS
	# ans = []
	queue = collections.deque()
	queue.append(beginWord)
	parents = collections.defaultdict(set)
	visited = set([beginWord])
	found = False 
	depth = 0
	while queue and not found:
		depth += 1 
		length = len(queue)
		# print(queue)
		localVisited = set()
		for _ in range(length):
			word = queue.popleft()
			for i in range(L):
				for nextWord in all_combo_dict[word[:i] + "*" + word[i+1:]]:
					if nextWord == word:
						continue
					if nextWord not in visited:
						parents[nextWord].add(word)
						if nextWord == endWord:    
							found = True
						localVisited.add(nextWord)
						queue.append(nextWord)
		visited = visited.union(localVisited)
	# print(parents)
	# Search path, DFS
	ans = []
	def dfs(node, path, d):
		if d == 0:
			if path[-1] == beginWord:
				ans.append(path[::-1])
			return 
		for parent in parents[node]:
			path.append(parent)
			dfs(parent, path, d-1)
			path.pop()
	dfs(endWord, [endWord], depth)
	return ans
