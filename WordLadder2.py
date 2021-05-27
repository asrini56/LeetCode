#Time - O(M^2 * N), M is length of words and N is total number of words in i/p list
import collections
class Solution:
    def findLadders(self, beginWord, endWord, wordList):
        # Edge cases
        if not beginWord or not endWord or not wordList:
            return []
        if endWord not in wordList or not len(beginWord) == len(endWord):
            return []

        n = len(beginWord)

        combs = collections.defaultdict(list)

        # Dict of patterns
        for word in wordList:
            for i in range(n):
                pattern = word[:i] + "*" + word[i + 1:]
                combs[pattern].append(word)

        # Ensure shortest path, because longer solutions get attached to the right
        queue = collections.deque([(beginWord, [])])
		
		# Avoid loops
        visited = set()
		
		# Solution space
        solutions = []
        min_solution_length = float("inf")

        while queue:
            # Pop word and mark as visited
            word, path_to_word = queue.popleft()
            visited.add(word)

            # Path to next word
            next_path = path_to_word + [word]
            if len(next_path) > min_solution_length:
                # Smaller solutions have been found. Return.
                return solutions

            # Small solution found
            if word == endWord:
                print(next_path)
                solutions.append(next_path)
                min_solution_length = len(next_path)

            # No solution found
            for i in range(n):
                pattern = word[:i] + "*" + word[i + 1:]
                for next_word in combs[pattern]:
                    if next_word not in visited:
                        queue.append((next_word, next_path))

        return solutions
