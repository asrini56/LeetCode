class Solution:
    def __init__(self):
        self.trie = {}
        self.end = "*"
        self.result = []
    def addWordToTrie(self,wordDict):
        for word in wordDict:
            node = self.trie
            for letter in word:
                if letter not in node:
                    node[letter] = {}
                node = node[letter]
            node[self.end] = word
    def searchWord(self,word):
        node = self.trie
        for letter in word:
            if letter not in node:
                return False
            node = node[letter]
        if "*" in node and node[self.end] == word:
            return True
                
    def dfs(self,s,sentance,pos):
        if pos == len(s):
            self.result.append(sentance)
            return
        for i in range(pos,len(s)):
            if self.searchWord(s[pos:i+1]):
                self.dfs(s,sentance+" "+s[pos:i+1],i+1)
    
    def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
        if not s or not wordDict:
            return []
        self.addWordToTrie(wordDict)
        for i in range(len(s)):
            if self.searchWord(s[:i+1]):
                remain = s[i+1:]
                self.dfs(s,s[:i+1],i+1)
        return self.result
