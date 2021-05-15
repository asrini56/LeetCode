#472. Concatenated Words
import collections

class TrieNode:
    def __init__(self):
        self.children = collections.defaultdict(TrieNode)
        self.isEnd = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        marker = self.root
        for ch in word:
            marker = marker.children[ch]
        marker.isEnd = True


class Solution:
    def findAllConcatenatedWordsInADict(self, words):
        
        def dfs(word, start, root, count):
            n = len(word)
            marker = root
            for i in range(start, n):
                marker = marker.children[word[i]]
                if marker.isEnd:           # smaller word encountered
                    if i == n-1:               # leaf node
                        return count>=1
                    elif dfs(word, i+1, root, count+1):     # increment the count and start a new DFS
                        return True
            return False
        
        res = []
        trie = Trie()
        for word in words:
            trie.insert(word)

        for word in words:
            if dfs(word, 0, trie.root, 0):
                res += word,
        
        return res
