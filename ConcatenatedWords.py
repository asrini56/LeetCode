#472. Concatenated Words
"""
time complexity would be m * w * n ^2
where,
m = number of words in concatenated words
w = maximum length of word in concatenated words
n = length of words

"""
import collections

class Trie:
    def __init__(self):
        self.root = {}
        self.endSymbol = "*"
    
    def addWords(self,word):
        node = self.root
        for w in word:
            if w not in node:
                node[w] = {}
            node = node[w]
        node[self.endSymbol] = True

class Solution:
    def findAllConcatenatedWordsInADict(self, words):
        
        def dfs(word,start,root,count,endSymbol):
            #Search a Word in Trie
            node = root
            for i in range(start,len(word)):
                if word[i] in node:
                    node = node[word[i]]
                    if endSymbol in node:
                        if i == len(word)-1:
                            return count >= 1
                        elif dfs(word,i+1,root,count+1,endSymbol):
                            return True
                else:
                    break
            return False
        trie = Trie()
        for word in words:
            trie.addWords(word)
        ans = []
        for word in words:
            if dfs(word,0,trie.root,0,trie.endSymbol):
                ans.append(word)
        return ans
