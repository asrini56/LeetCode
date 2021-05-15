#211. Design Add and Search Words Data Structure, Time - O(N * (26^M))
class WordDictionary:

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = {}
        self.endSymbol = "*"
        

    def addWord(self, word: str) -> None:
        node = self.root
        for w in word:
            if w not in node:
                node[w] = {}
            node = node[w]
        node[self.endSymbol] = True

    def search(self, word: str) -> bool:
        def search_in_word(word,node):
            for i,w in enumerate(word):
                if w not in node:
                    if w == '.':
                        for x in node:
                            if x != self.endSymbol and search_in_word(word[i + 1:], node[x]):
                                return True
                    return False
                else:
                    node = node[w]
            if self.endSymbol in node:
                return True
        return search_in_word(word,self.root)


# Your WordDictionary object will be instantiated and called as such:
# obj = WordDictionary()
# obj.addWord(word)
# param_2 = obj.search(word)
