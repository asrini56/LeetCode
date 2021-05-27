class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
		# instantiate an empty trie 
        trie = Trie()
        # Iterate over words in dictionary and build trie one word at a time
        for word in wordDict:   #------ O(W) where W = len(words)
            trie.add(word)  #--------------- O(K) where K = len(word)
        # Words have been added. Find if s is made up of words in the trie
        return trie.find(s)  # ---- Overall time : O(W*K) OR O(S*S[i+1:]) Whichever is worst

class Node:
    def __init__(self, val):
        self.val = val
        self.children = {}
        self.is_done = False

class Trie:
    def __init__(self):
        self.root = Node(None)
        self.memo = {}

    def add(self, word):
        root = self.root
        for char in word:
            if char not in root.children:
                root.children[char] = Node(char)
            root = root.children[char]
        root.is_done = True
    def find(self, s):
        root = self.root
        for i, char in enumerate(s):
            if char not in root.children:
                return False
            
            if root.children[char].is_done:
                if s[i+1:] not in self.memo:
                    self.memo[s[i+1:]] = self.find(s[i+1:])
                if self.memo[s[i+1:]]:
                    return True
            root = root.children[char]
        return root.is_done 
